from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import TorneoTCG, FranquiciaTCG
from .forms import TorneoTCGForm


def es_staff_o_admin(user):
    return user.is_authenticated and user.is_staff


def torneo_lista(request):
    """Catálogo público de torneos con búsqueda, filtros y ordenamiento"""
    franquicias = FranquiciaTCG.objects.filter(activo=True)
    franquicia_slug = request.GET.get('franquicia', '').strip()
    query = request.GET.get('q', '').strip()
    orden = request.GET.get('orden', 'fecha_asc')

    torneos = TorneoTCG.objects.filter(activo=True).select_related('franquicia')

    if franquicia_slug:
        torneos = torneos.filter(franquicia__slug=franquicia_slug)

    if query:
        torneos = torneos.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(formato__icontains=query) |
            Q(lugar__icontains=query)
        )

    # Ordenamiento
    orden_mapping = {
        'fecha_asc': 'fecha_evento',
        'precio_asc': 'precio_inscripcion',
        'precio_desc': '-precio_inscripcion',
        'nombre_asc': 'nombre',
    }
    campo_orden = orden_mapping.get(orden, 'fecha_evento')
    torneos = torneos.order_by(campo_orden)

    context = {
        'franquicias': franquicias,
        'torneos': torneos,
        'franquicia_seleccionada': franquicia_slug,
        'query_actual': query,
        'orden_actual': orden,
        'total_resultados': torneos.count(),
    }
    return render(request, 'catalogo/torneo_lista.html', context)


def torneo_detalle(request, slug):
    """Ficha técnica detallada de un torneo individual"""
    if request.user.is_staff:
        torneo = get_object_or_404(TorneoTCG.objects.select_related('franquicia'), slug=slug)
    else:
        torneo = get_object_or_404(TorneoTCG.objects.select_related('franquicia'), slug=slug, activo=True)

    relacionados = TorneoTCG.objects.filter(
        franquicia=torneo.franquicia, 
        activo=True
    ).exclude(id=torneo.id).order_by('fecha_evento')[:3]

    return render(request, 'catalogo/torneo_detalle.html', {
        'torneo': torneo,
        'relacionados': relacionados
    })


@login_required
@user_passes_test(es_staff_o_admin)
def torneo_gestion(request):
    """Panel de control operativo de eventos para organizadores y jueces"""
    query = request.GET.get('q', '').strip()
    torneos = TorneoTCG.objects.all().select_related('franquicia').order_by('-fecha_evento')

    if query:
        torneos = torneos.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(formato__icontains=query)
        )

    return render(request, 'catalogo/torneo_gestion.html', {
        'torneos': torneos,
        'query': query,
        'total_torneos': torneos.count()
    })


@login_required
@user_passes_test(es_staff_o_admin)
def torneo_crear(request):
    """Formulario para publicar un nuevo torneo en la plataforma"""
    if request.method == 'POST':
        form = TorneoTCGForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_torneo = form.save()
            messages.success(request, f"Torneo '{nuevo_torneo.nombre}' creado exitosamente.")
            return redirect('catalogo:gestion')
    else:
        form = TorneoTCGForm()

    return render(request, 'catalogo/torneo_form.html', {
        'form': form,
        'titulo': "Publicar Nuevo Torneo",
        'accion': "Crear Evento"
    })


@login_required
@user_passes_test(es_staff_o_admin)
def torneo_editar(request, pk):
    """Formulario de edición para modificar datos, cupos o estado de un torneo"""
    torneo = get_object_or_404(TorneoTCG, pk=pk)

    if request.method == 'POST':
        form = TorneoTCGForm(request.POST, request.FILES, instance=torneo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Torneo '{torneo.nombre}' actualizado correctamente.")
            return redirect('catalogo:gestion')
    else:
        form = TorneoTCGForm(instance=torneo)

    return render(request, 'catalogo/torneo_form.html', {
        'form': form,
        'torneo': torneo,
        'titulo': f"Editar Torneo: {torneo.codigo}",
        'accion': "Guardar Cambios"
    })


@login_required
@user_passes_test(es_staff_o_admin)
def torneo_eliminar(request, pk):
    """Confirmación y eliminación de un torneo del catálogo"""
    torneo = get_object_or_404(TorneoTCG, pk=pk)

    if request.method == 'POST':
        nombre = torneo.nombre
        torneo.delete()
        messages.warning(request, f"El torneo '{nombre}' ha sido eliminado definitivamente.")
        return redirect('catalogo:gestion')

    return render(request, 'catalogo/torneo_confirmar_eliminar.html', {'torneo': torneo})
