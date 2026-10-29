from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='home_repuestos'),
    path('crear/', views.crear_repuesto, name='crear_repuesto'),
    path('detalle/<int:repuesto_id>/', views.detalle_repuesto, name='detalle_repuesto'),
    path('editar/<int:repuesto_id>/', views.editar_repuesto, name='editar_repuesto'),
    path('eliminar/<int:repuesto_id>/', views.eliminar_repuesto, name='eliminar_repuesto'),
]