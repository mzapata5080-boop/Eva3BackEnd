from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.torneo_lista, name='lista'),
    path('gestion/', views.torneo_gestion, name='gestion'),
    path('gestion/crear/', views.torneo_crear, name='crear'),
    path('gestion/editar/<int:pk>/', views.torneo_editar, name='editar'),
    path('gestion/eliminar/<int:pk>/', views.torneo_eliminar, name='eliminar'),
    path('<slug:slug>/', views.torneo_detalle, name='detalle'),
]

