from django.urls import path
from reparacionesApp import views

urlpatterns = [
    path('', views.principal_reparaciones, name='inicio_reparaciones'),
    path('registrar/', views.registrar_reparacion, name= 'registrar_reparacion')
]