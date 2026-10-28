from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from vehiculosApp import views 
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehiculos/', include('vehiculosApp.urls')),
    path('repuestos/', include('repuestosApp.urls')),
    path('empleados/', include('empleadosApp.urls')),
    path('clientes/', include('clientesApp.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('principal/', views.menu_principal, name="menu-principal"),
    path('login/', include('usuarios.urls'), name="login"),
    path('reparaciones/', include('reparacionesApp.urls'), name='home_reparaciones'),
    path('usuarios/', usuarios_views.principal_usuarios, name='inicio_usuarios'),
    path('', include('dashboardApp.urls'), name= 'dashboard_inicio')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)