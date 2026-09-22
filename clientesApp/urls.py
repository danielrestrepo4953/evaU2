from django.urls import path
from clientesApp import views

urlpatterns = [
    path('', views.lista_clientes, name='home_clientes'),
    path('detalle/<str:nombre>/', views.detalle_cliente, name='detalle_cliente'),
]