from django.shortcuts import render
from apps.catalogo.models import TorneoTCG, FranquiciaTCG
from django.contrib.auth.models import User
from django.utils import timezone

def inicio(request):
    """Página principal inspirada en Torneos TCG para la comunidad de Chillán"""
    torneos_destacados = TorneoTCG.objects.filter(destacado=True, activo=True).select_related('franquicia')[:3]
    proximos_torneos = TorneoTCG.objects.filter(activo=True).select_related('franquicia').order_by('fecha_evento')[:6]
    franquicias = FranquiciaTCG.objects.filter(activo=True)
    
    # "Los Tres Grandes" TCGs (Pokémon, One Piece, Magic) con sus torneos en Chillán
    tres_grandes_nombres = ['Pokémon TCG', 'One Piece Card Game', 'Magic: The Gathering']
    tres_grandes = []
    for nombre in tres_grandes_nombres:
        franq = FranquiciaTCG.objects.filter(nombre__icontains=nombre.split()[0]).first()
        if franq:
            torneos_franq = TorneoTCG.objects.filter(franquicia=franq, activo=True).order_by('fecha_evento')[:5]
            tres_grandes.append({
                'franquicia': franq,
                'torneos': torneos_franq,
                'total_torneos': TorneoTCG.objects.filter(franquicia=franq, activo=True).count(),
            })

    # Tiendas / Sedes oficiales en Chillán
    tiendas_chillan = [
        {"nombre": "La Ira", "ciudad": "Chillán", "detalle": "Especialistas en Magic, Pokémon y TCG competitivo."},
        {"nombre": "Suna Senso", "ciudad": "Chillán", "detalle": "Comunidad activa de torneos, ligas y casual play."},
        {"nombre": "Rey Mago", "ciudad": "Chillán", "detalle": "Duelos de Yu-Gi-Oh!, One Piece y cartas coleccionables."},
    ]

    total_torneos = TorneoTCG.objects.filter(activo=True).count()
    total_franquicias = franquicias.count()
    total_jugadores = User.objects.filter(is_active=True).count()

    context = {
        'torneos_destacados': torneos_destacados,
        'proximos_torneos': proximos_torneos,
        'tres_grandes': tres_grandes,
        'tiendas_chillan': tiendas_chillan,
        'franquicias': franquicias,
        'total_torneos': total_torneos,
        'total_franquicias': total_franquicias,
        'total_jugadores': total_jugadores,
        'fecha_hoy': timezone.localtime(),
    }
    return render(request, 'core/inicio.html', context)


def nosotros(request):
    """Información institucional, reglamento y sedes de la liga"""
    franquicias = FranquiciaTCG.objects.filter(activo=True)
    return render(request, 'core/nosotros.html', {'franquicias': franquicias})
