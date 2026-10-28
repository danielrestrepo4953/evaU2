from django.urls import path
from clientesApp import views

urlpatterns = [
    path('', views.lista_clientes, name='home_clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('detalle/<str:nombre>/', views.detalle_cliente, name='detalle_cliente'),
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
]