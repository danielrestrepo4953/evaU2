from django.urls import path
from compraRepuestosApp import views

urlpatterns = [
    path('', views.principal_ventas, name='inicio_compras'),
    path('registrar/', views.registrar_compra, name='registrar_compra'),
    path('editar/<int:compra_id>/', views.editar_compra, name='editar_compra'),
    path('eliminar/<int:compra_id>/', views.eliminar_compra, name='eliminar_compra'),
]