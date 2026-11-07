from django.contrib import admin
from .models import FranquiciaTCG, TorneoTCG

admin.site.site_header = "TCG League Master - Panel de Control Operativo"
admin.site.site_title = "TCG League Admin"
admin.site.index_title = "Gestión de Torneos, Formatos y Jugadores"


@admin.register(FranquiciaTCG)
class FranquiciaTCGAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'editorial', 'slug', 'activo', 'creado_en')
    search_fields = ('nombre', 'editorial', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ('activo',)


@admin.register(TorneoTCG)
class TorneoTCGAdmin(admin.ModelAdmin):
    list_display = (
        'codigo', 'nombre', 'franquicia', 'formato', 
        'precio_formateado', 'cupos_disponibles', 'estado', 'activo', 'destacado'
    )
    list_filter = ('franquicia', 'estado', 'activo', 'destacado', 'fecha_evento')
    search_fields = ('codigo', 'nombre', 'formato', 'lugar')
    list_editable = ('cupos_disponibles', 'estado', 'activo', 'destacado')
    prepopulated_fields = {'slug': ('codigo', 'nombre')}
    list_per_page = 15
    
    fieldsets = (
        ('Identificación del Evento', {
            'fields': ('codigo', 'nombre', 'slug', 'franquicia', 'formato')
        }),
        ('Planificación y Aforo', {
            'fields': ('fecha_evento', 'lugar', 'precio_inscripcion', 'cupos_maximos', 'cupos_disponibles')
        }),
        ('Estado Operativo y Presentación', {
            'fields': ('estado', 'afiche', 'destacado', 'activo')
        }),
    )
