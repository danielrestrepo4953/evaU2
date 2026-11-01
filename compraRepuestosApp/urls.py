from django.urls import path
from compraRepuestosApp import views

urlpatterns = [
    path('', views.principal_ventas, name='inicio_compras'),
    path('registrar/', views.registrar_compra, name= 'registrar_compra')
]