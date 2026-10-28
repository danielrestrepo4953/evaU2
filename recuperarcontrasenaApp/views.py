from hashlib import sha256

from django.contrib.auth import views as auth_views
from django.core.cache import cache
from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm

def obtener_ip(request):
    return request.META.get('REMOTE_ADDR', 'ip-desconocida')


def crear_clave_correo(email):
    return sha256(email.encode('utf-8')).hexdigest()


class SolicitarRecuperacionView(auth_views.PasswordResetView):
    template_name = 'recuperarcontrasena/solicitar.html'
    email_template_name = (
        'recuperarcontrasena/correo_recuperacion.txt'
    )
    html_email_template_name = (
        'recuperarcontrasena/correo_recuperacion.html'
    )
    subject_template_name = (
        'recuperarcontrasena/asunto_correo.txt'
    )
    success_url = '/recuperar-contrasena/enviado/'
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '').strip().lower()
        ip = obtener_ip(request)

        clave_ip = f'password-reset-ip:{ip}'
        solicitudes_ip = cache.get(clave_ip, 0)

        if solicitudes_ip >= 5:
            return render(
                request,
                'recuperarcontrasena/limite.html',
            )

        cache.set(clave_ip, solicitudes_ip + 1, 900)

        if email:
            clave_email = (
                f'password-reset-email:{crear_clave_correo(email)}'
            )
            solicitudes_email = cache.get(clave_email, 0)

            if solicitudes_email >= 3:
                return render(
                    request,
                    'recuperarcontrasena/limite.html',
                )

            cache.set(clave_email, solicitudes_email + 1, 900)

        return super().post(request, *args, **kwargs)