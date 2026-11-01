from django.urls import path
from asignacionesApp import views

urlpatterns = [
    path('', views.inicio_asignaciones, name='inicio_asignaciones'),
    path('registrar/', views.registrar_asignacion, name='registrar_asignacion'),
    path('editar/<int:asignacion_id>/', views.editar_asignacion, name='editar_asignacion'),
    path('eliminar/<int:asignacion_id>/', views.eliminar_asignacion, name='eliminar_asignacion'),
]
