from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from vehiculosApp import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehiculos/', include('vehiculosApp.urls')),
    path('repuestos/', include('repuestosApp.urls')),
    path('empleados/', include('empleadosApp.urls')),
    path('clientes/', include('clientesApp.urls')),
    path('', views.menu_principal, name="menu-principal"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)