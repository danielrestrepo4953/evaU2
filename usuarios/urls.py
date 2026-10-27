from django.contrib.auth import views as auth_views
from django.urls import path
from usuarios import views as usuarios_views


urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),

    path('', usuarios_views.principal_usuarios, name='inicio_usuarios'),
    path('crear/', usuarios_views.crear_usuario, name='crear_usuario'),
    path('editar/<int:usuario_id>/', usuarios_views.cargar_editar_usuario, name='cargar_editar_usuario'),
    path('editarcambios/<int:usuario_id>/', usuarios_views.editar_usuario, name='editar_usuario'),
    path('eliminarusuario/<int:usuario_id>/', usuarios_views.eliminar_usuario, name= 'eliminar_usuario')
]
