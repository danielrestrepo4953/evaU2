from io import BytesIO
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import repuestos


class RepuestoCrudTests(TestCase):
    def setUp(self):
        self.media_directory = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.settings_override.enable()
        user = get_user_model().objects.create_user(username='usuario', password='clave-segura')
        self.client.force_login(user)

    def tearDown(self):
        self.settings_override.disable()
        self.media_directory.cleanup()

    def test_create_edit_and_delete_repuesto(self):
        image_buffer = BytesIO()
        Image.new('RGB', (1, 1)).save(image_buffer, format='PNG')
        image = SimpleUploadedFile('repuesto.png', image_buffer.getvalue(), content_type='image/png')
        response = self.client.post(reverse('crear_repuesto'), {
            'codigo': 'REP-001',
            'nombre': 'Bujía',
            'precio': 5000,
            'stock': 3,
            'detalle': 'Bujía de prueba',
            'imagen': image,
        })

        self.assertRedirects(response, reverse('home_repuestos'))
        repuesto = repuestos.objects.get(codigo='REP-001')
        image_name = repuesto.imagen.name

        response = self.client.post(reverse('editar_repuesto', args=[repuesto.id]), {
            'codigo': 'REP-001',
            'nombre': 'Bujía actualizada',
            'precio': 6000,
            'stock': 4,
            'detalle': 'Detalle actualizado',
        })
        self.assertRedirects(response, reverse('home_repuestos'))
        repuesto.refresh_from_db()
        self.assertEqual(repuesto.nombre, 'Bujía actualizada')
        self.assertEqual(repuesto.precio, 6000)
        self.assertEqual(repuesto.imagen.name, image_name)

        response = self.client.get(reverse('eliminar_repuesto', args=[repuesto.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('eliminar_repuesto', args=[repuesto.id]))
        self.assertRedirects(response, reverse('home_repuestos'))
        self.assertFalse(repuestos.objects.filter(id=repuesto.id).exists())
