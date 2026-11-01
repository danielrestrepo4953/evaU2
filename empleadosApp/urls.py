from django.urls import path
from empleadosApp import views
urlpatterns = [
    path('', views.principal, name="principal" ),
    path('detalle/<int:id>/', views.detalle, name="detalle" ),
    path('registrar/', views.registrar_empleado, name="registrar_empleado" ),
    path('editar/<int:id>/', views.editar_empleado, name="editar_empleado" ),
    path('eliminar/<int:id>/', views.eliminar_empleado, name="eliminar_empleado" ),
]
