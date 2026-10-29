from django.urls import path
from clientesVehiculosApp import views

urlpatterns = [
    path('', views.lista_clientes_vehiculos, name='lista_clientes_vehiculos'),
    path('asociar/', views.asociar_cliente_vehiculo, name='asociar_cliente_vehiculo'),
    path('editar/<int:asociacion_id>/', views.editar_asociacion, name='editar_asociacion'),
    path('eliminar/<int:asociacion_id>/', views.eliminar_asociacion, name='eliminar_asociacion'),
]