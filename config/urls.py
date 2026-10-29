from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from vehiculosApp import views
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehiculos/', include('vehiculosApp.urls')),
    path('repuestos/', include('repuestosApp.urls')),
    path('empleados/', include('empleadosApp.urls')),
    path('compras/', include('compraRepuestosApp.urls')),
    path('compra-repuestos/', include(('compraRepuestosApp.urls', 'compras_legacy'), namespace='compras_legacy')),
    path('clientes/', include('clientesApp.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('', views.menu_principal, name="menu-principal"),
    path('login/', include('usuarios.urls'), name="login"),
    path('reparaciones/', include('reparacionesApp.urls'), name='home_reparaciones'),
    path('asignaciones/', include('asignacionesApp.urls')),
    path('clientes-vehiculos/', include('clientesVehiculosApp.urls')),
    path('usuarios/', usuarios_views.principal_usuarios, name='inicio_usuarios'),
    path('dashboard/', include('dashboardApp.urls'), name='dashboard_inicio'),
    path('recuperar-contrasena/', include('recuperarcontrasenaApp.urls'), name='recuperar_contrasena'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
