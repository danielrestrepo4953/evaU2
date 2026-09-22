from django.urls import path
from empleadosApp import views
urlpatterns = [
    path('', views.principal, name="principal" ),
    path('detalle/<int:id>/', views.detalle, name="detalle" ),
]
