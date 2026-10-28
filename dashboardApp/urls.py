from django.urls import path
from . import views

urlpatterns = [
    path('', views.redireccionar_por_grupo, name='redireccionar_usuario'),
    path('dashboard_empleado/', views.cargar_dashboard_empleado, name= 'dashboard_empleado'),
    path('dashboard_supervisor/', views.cargar_dashboard_supervisor, name= 'dashboard_supervisor'),
    path('dashboard_administrador/', views.cargar_dashboard_administrador, name='dashboard_admin')
]