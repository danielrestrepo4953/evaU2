from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='home_repuestos'),
    path('detalle/<int:repuesto_id>/', views.detalle_repuesto, name='detalle_repuesto')
]