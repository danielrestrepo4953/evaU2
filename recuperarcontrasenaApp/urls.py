from django.contrib.auth import views as auth_views
from django.urls import path

from recuperarcontrasenaApp.views import SolicitarRecuperacionView


urlpatterns = [
    path(
        '',
        SolicitarRecuperacionView.as_view(),
        name='password_reset',
    ),
    path(
        'enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='recuperarcontrasena/enviado.html',
        ),
        name='password_reset_done',
    ),
    path(
        '<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='recuperarcontrasena/confirmar.html',
            success_url='/recuperar-contrasena/completada/',
        ),
        name='password_reset_confirm',
    ),
    path(
        'completada/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='recuperarcontrasena/completada.html',
        ),
        name='password_reset_complete',
    ),
]