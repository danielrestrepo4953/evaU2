from io import BytesIO
import tempfile

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from clientesApp.models import Cliente
from compraRepuestosApp.models import CompraRepuesto, DetalleCompra
from reparacionesApp.models import Reparacion, RepuestoUtilizado
from .models import repuestos
from vehiculosApp.models import Vehiculo


class RepuestoCrudTests(TestCase):
    def setUp(self):
        self.media_directory = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.settings_override.enable()
        user = get_user_model().objects.create_user(username='usuario', password='clave-segura')
        user.user_permissions.set(Permission.objects.filter(
            content_type__app_label='repuestosApp',
            codename__in=(
                'view_repuestos',
                'add_repuestos',
                'change_repuestos',
                'delete_repuestos',
            ),
        ))
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

    def test_usuario_sin_permisos_no_puede_acceder_por_url(self):
        usuario = get_user_model().objects.create_user(
            username='sin-permisos',
            password='clave-segura',
        )
        self.client.force_login(usuario)

        for nombre_url, args in (
            ('home_repuestos', ()),
            ('crear_repuesto', ()),
            ('editar_repuesto', (1,)),
            ('eliminar_repuesto', (1,)),
        ):
            response = self.client.get(reverse(nombre_url, args=args))
            self.assertEqual(response.status_code, 403)

    def test_no_permite_eliminar_repuesto_usado_en_compra(self):
        repuesto = repuestos.objects.create(
            codigo='REP-002',
            nombre='Filtro de aceite',
            precio=8000,
            stock=2,
            detalle='Filtro de prueba',
        )
        compra = CompraRepuesto.objects.create(
            cliente=Cliente.objects.create(nombre='Cliente de prueba'),
            proveedor='Proveedor de prueba',
        )
        DetalleCompra.objects.create(
            compra=compra,
            repuesto=repuesto,
            cantidad=1,
            precio_unitario=8000,
        )

        response = self.client.post(reverse('eliminar_repuesto', args=[repuesto.id]))

        self.assertRedirects(response, reverse('home_repuestos'))
        self.assertTrue(repuestos.objects.filter(id=repuesto.id).exists())
        self.assertContains(
            response,
            'No se puede eliminar el repuesto porque ha sido utilizado en compras o reparaciones.',
        )

    def test_no_permite_eliminar_repuesto_usado_en_reparacion(self):
        repuesto = repuestos.objects.create(
            codigo='REP-003',
            nombre='Pastillas de freno',
            precio=15000,
            stock=2,
            detalle='Pastillas de prueba',
        )
        reparacion = Reparacion.objects.create(
            vehiculo=Vehiculo.objects.create(
                marca='Marca de prueba',
                modelo='Modelo de prueba',
                anio=2024,
                patente='TEST-03',
            ),
            detalle='Reparacion de prueba',
        )
        RepuestoUtilizado.objects.create(
            reparacion=reparacion,
            repuesto=repuesto,
            cantidad=1,
        )

        response = self.client.post(reverse('eliminar_repuesto', args=[repuesto.id]))

        self.assertRedirects(response, reverse('home_repuestos'))
        self.assertTrue(repuestos.objects.filter(id=repuesto.id).exists())
        self.assertContains(
            response,
            'No se puede eliminar el repuesto porque ha sido utilizado en compras o reparaciones.',
        )
