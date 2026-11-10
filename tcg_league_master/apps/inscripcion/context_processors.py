def inscripciones_context(request):
    """Contador global de pre-inscripciones en la sesión"""
    inscripciones = request.session.get('inscripciones', {})
    total_items = sum(item.get('jugadores', 1) for item in inscripciones.values())
    return {
        'inscripciones_total_items': total_items
    }