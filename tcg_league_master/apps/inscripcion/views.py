from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.catalogo.models import TorneoTCG

# Create your views here.

def _obtener_inscripciones(request):
    return request.session.setdefault('inscripciones', {})


def inscripcion_ver(request):
    """Muestra la canasta temporal de inscripciones con desglose numérico/económico"""
    inscripciones = _obtener_inscripciones(request)
    subtotal = sum(item['subtotal'] for item in inscripciones.values())
    recargo_servicio = int(subtotal * 0.05) # 5% recargo por comisión de juez/sistema
    total = subtotal + recargo_servicio
    return render(request, 'inscripcion/inscripciones.html', {
        'items': inscripciones.values(),
        'subtotal': subtotal,
        'recargo_servicio': recargo_servicio,
        'total': total,
        'esta_vacio': len(inscripciones) == 0,
    })


def inscripcion_agregar(request, id):
    torneo = get_object_or_404(TorneoTCG, id=id, activo=True)
    if not torneo.hay_cupos:
        messages.error(request, f"El torneo '{torneo.nombre}' no tiene cupos disponibles o no está abierto.")
        return redirect('catalogo:lista')

    inscripciones = _obtener_inscripciones(request)
    str_id = str(torneo.id)

    if str_id in inscripciones:
        messages.info(request, f"Ya tienes pre-reservado un cupo para '{torneo.nombre}'.")
    else:
        afiche_url = torneo.afiche.url if torneo.afiche else ''
        inscripciones[str_id] = {
            'id': torneo.id,
            'codigo': torneo.codigo,
            'nombre': torneo.nombre,
            'slug': torneo.slug,
            'franquicia': torneo.franquicia.nombre,
            'formato': torneo.formato,
            'precio': int(torneo.precio_inscripcion),
            'jugadores': 1,
            'subtotal': int(torneo.precio_inscripcion),
            'afiche_url': afiche_url,
            'fecha': torneo.fecha_evento.strftime('%d/%m/%Y %H:%M'),
        }
        request.session.modified = True
        messages.success(request, f"Te has pre-inscrito temporalmente a '{torneo.nombre}'.")

    return redirect(request.META.get('HTTP_REFERER') or 'inscripcion:ver')


def inscripcion_eliminar(request, id):
    inscripciones = _obtener_inscripciones(request)
    str_id = str(id)
    if str_id in inscripciones:
        del inscripciones[str_id]
        request.session.modified = True
        messages.warning(request, "Pre-inscripción removida.")
    return redirect('inscripcion:ver')


def inscripcion_limpiar(request):
    if 'inscripciones' in request.session:
        del request.session['inscripciones']
        request.session.modified = True
    return redirect('inscripcion:ver')


@login_required
def resumen_confirmacion(request):
    """Simula la confirmación final del pre-agendamiento y vacía la sesión"""
    inscripciones = _obtener_inscripciones(request)
    if not inscripciones:
        return redirect('catalogo:lista')

    subtotal = sum(item['subtotal'] for item in inscripciones.values())
    recargo_servicio = int(subtotal * 0.05)
    total = subtotal + recargo_servicio
    items_confirmados = list(inscripciones.values())

    # Descuenta cupos en la base de datos
    for item in items_confirmados:
        try:
            t = TorneoTCG.objects.get(id=item['id'])
            if t.cupos_disponibles > 0:
                t.cupos_disponibles -= 1
                t.save()
        except TorneoTCG.DoesNotExist:
            pass

    del request.session['inscripciones']
    request.session.modified = True

    return render(request, 'inscripcion/comprobante_exito.html', {
        'items': items_confirmados,
        'subtotal': subtotal,
        'recargo': recargo_servicio,
        'total': total,
        'codigo_reserva': f"TCG-{request.user.id}-2026",
    })