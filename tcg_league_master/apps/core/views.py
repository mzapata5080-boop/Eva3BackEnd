from django.shortcuts import render
from apps.catalogo.models import TorneoTCG, FranquiciaTCG
from django.contrib.auth.models import User

def inicio(request):
    """Página principal de bienvenida de TCG League Master"""
    torneos_destacados = TorneoTCG.objects.filter(destacado=True, activo=True).select_related('franquicia')[:3]
    proximos_torneos = TorneoTCG.objects.filter(activo=True).select_related('franquicia').order_by('fecha_evento')[:6]
    franquicias = FranquiciaTCG.objects.filter(activo=True)
    
    total_torneos = TorneoTCG.objects.filter(activo=True).count()
    total_franquicias = franquicias.count()
    total_jugadores = User.objects.filter(is_active=True).count()

    context = {
        'torneos_destacados': torneos_destacados,
        'proximos_torneos': proximos_torneos,
        'franquicias': franquicias,
        'total_torneos': total_torneos,
        'total_franquicias': total_franquicias,
        'total_jugadores': total_jugadores,
    }
    return render(request, 'core/inicio.html', context)


def nosotros(request):
    """Información institucional, reglamento y sedes de la liga"""
    franquicias = FranquiciaTCG.objects.filter(activo=True)
    return render(request, 'core/nosotros.html', {'franquicias': franquicias})
