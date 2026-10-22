from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='usuario_prueba',
            password='UnaClaveSegura123!',
        )

    def test_login_creates_authenticated_session(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'usuario_prueba',
                'password': 'UnaClaveSegura123!',
            },
        )

        self.assertRedirects(response, reverse('menu-principal'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_credentials_do_not_create_session(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'usuario_prueba',
                'password': 'clave_incorrecta',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_clears_authenticated_session(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('menu-principal'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
