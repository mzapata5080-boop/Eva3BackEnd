from django.urls import path
from . import views

app_name = 'inscripcion'

urlpatterns = [
    path('', views.inscripcion_ver, name='ver'),
    path('agregar/<int:id>/', views.inscripcion_agregar, name='agregar'),
    path('eliminar/<int:id>/', views.inscripcion_eliminar, name='eliminar'),
    path('limpiar/', views.inscripcion_limpiar, name='limpiar'),
    path('confirmar/', views.resumen_confirmacion, name='confirmar'),
]

