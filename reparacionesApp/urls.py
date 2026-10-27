from django.urls import path
from reparacionesApp import views

urlpatterns = [
    path('', views.principal_reparaciones, name='inicio_reparaciones'),
    path('registrar/', views.registrar_reparacion, name= 'registrar_reparacion'),
    path('cargar_editar_reparacion/<int:reparacion_id>/', views.cargar_editar_reparacion, name='cargar_editar_reparacion'),
    path('editar_reparacion/<int:reparacion_id>/', views.editar_reparacion, name='editar_reparacion'),
    path('eliminar_reparacion/<int:reparacion_id>/', views.eliminar_reparacion, name= 'eliminar_reparacion')
]