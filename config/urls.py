from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from vehiculosApp import views
from repuestosApi import views as api_vistas
from usuarios import views as usuarios_views
from repuestosApp import views as vista
from empleadosApp import api_views as empleados_api
from compraRepuestosApp import api_views as compras_api
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
    path('principal/', views.menu_principal, name="menu-principal-alias"),
    path('login/', include('usuarios.urls'), name="login"),
    path('reparaciones/', include('reparacionesApp.urls'), name='home_reparaciones'),
    path('asignaciones/', include('asignacionesApp.urls')),
    path('clientes-vehiculos/', include('clientesVehiculosApp.urls')),
    path('usuarios/', usuarios_views.principal_usuarios, name='inicio_usuarios'),
    path('dashboard/', include('dashboardApp.urls'), name='dashboard_inicio'),
    path('api/repuestos/', api_vistas.repuestos, name='api_repuestos'),
    path('api/repuestos_lista/', api_vistas.repuesto_lista, name='repuestos_lista'),
    path('api/repuestos_detalle/<int:pk>/', api_vistas.repuesto_detalle, name= 'repuestos_detalle'),
    path('api/empleados/', empleados_api.empleado_lista, name='empleados_lista'),
    path('api/empleados/<int:pk>/', empleados_api.empleado_detalle, name='empleados_detalle'),
    path('api/compras/', compras_api.compra_lista, name='compras_lista'),
    path('api/compras/<int:pk>/', compras_api.compra_detalle, name='compras_detalle'),
    # ruta documentacion de la API
    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('api/swagger/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc'),
    path('exportar_repuestos_excel/', vista.exportar_repuestos_excel, name= 'exportar_repuestos_excel'),
    path('exportar_repuestos_pdf/', vista.exportar_repuestos_pdf, name= 'exportar_repuestos_pdf'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name= 'token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
