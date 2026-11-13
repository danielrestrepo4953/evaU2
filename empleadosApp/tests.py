import io
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from asignacionesApp.models import Asignacion
from empleadosApp.models import Empleado, DetalleEmpleado
from vehiculosApp.models import Vehiculo


class EmpleadosTests(TestCase):

    def setUp(self):
        User = get_user_model()
        permisos = Permission.objects.filter(content_type__app_label='empleadosApp')

        self.admin = User.objects.create_user('admin_test', password='clave-test-123')
        self.admin.user_permissions.set(permisos)

        self.solo_lectura = User.objects.create_user('lector_test', password='clave-test-123')
        self.solo_lectura.user_permissions.add(permisos.get(codename='view_empleado'))

        self.empleado = Empleado.objects.create(rut='11.111.111-1', nombre='Ana', apellido='Rojas', cargo='Mecánico')
        DetalleEmpleado.objects.create(empleado=self.empleado, direccion='La Serena',
                                       telefono='+56 9 1111 1111', correo='ana@empresa.cl')

    def datos(self, **cambios):
        datos = {
            'rut': '12345678-5',
            'nombre': 'Luis',
            'apellido': 'Soto',
            'cargo': 'Chofer',
            'direccion': 'Coquimbo',
            'fecha_contratacion': '2025-03-15',
            'telefono': '+56 9 1234 5678',
            'correo': 'luis@empresa.cl',
        }
        datos.update(cambios)
        return datos

    def test_sin_login_redirige_al_login(self):
        for url in [reverse('principal'), reverse('registrar_empleado'),
                    reverse('editar_empleado', args=[self.empleado.id]),
                    reverse('eliminar_empleado', args=[self.empleado.id])]:
            respuesta = self.client.get(url)
            self.assertEqual(respuesta.status_code, 302)
            self.assertIn('/login/', respuesta.url)

    def test_usuario_solo_lectura_no_puede_crear_editar_ni_eliminar(self):
        self.client.force_login(self.solo_lectura)
        self.assertEqual(self.client.get(reverse('principal')).status_code, 200)
        self.assertEqual(self.client.get(reverse('registrar_empleado')).status_code, 403)
        self.assertEqual(self.client.get(reverse('editar_empleado', args=[self.empleado.id])).status_code, 403)
        self.assertEqual(self.client.get(reverse('eliminar_empleado', args=[self.empleado.id])).status_code, 403)

    def test_registrar_empleado_con_detalle_y_rut_normalizado(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('registrar_empleado'), self.datos())
        self.assertRedirects(respuesta, reverse('principal'))
        nuevo = Empleado.objects.get(nombre='Luis')
        self.assertEqual(nuevo.rut, '12.345.678-5')
        self.assertEqual(nuevo.detalle.correo, 'luis@empresa.cl')

    def test_rut_repetido_escrito_distinto(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('registrar_empleado'), self.datos(rut='11111111-1'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Empleado.objects.count(), 1)

    def test_rut_repetido_guardado_sin_puntos(self):
        Empleado.objects.create(rut='36185683-9', nombre='Luis', apellido='Diaz', cargo='Vendedor')
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('registrar_empleado'), self.datos(rut='36.185.683-9'))
        self.assertContains(respuesta, 'Ya existe un empleado registrado con este RUT')
        self.assertEqual(Empleado.objects.count(), 2)

    def test_validaciones_del_formulario(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('registrar_empleado'), self.datos(
            rut='abc', nombre='L1', telefono='12ab', correo='no-es-correo', fecha_contratacion='2999-01-01'))
        self.assertContains(respuesta, 'El RUT debe tener el formato')
        self.assertContains(respuesta, 'solo puede contener letras')
        self.assertContains(respuesta, 'El teléfono solo puede contener')
        self.assertContains(respuesta, 'no puede ser mayor a la fecha actual')
        self.assertEqual(Empleado.objects.count(), 1)

    def test_editar_empleado(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('editar_empleado', args=[self.empleado.id]),
                                     self.datos(rut='11.111.111-1', nombre='Ana María', cargo='Jefa de taller'))
        self.assertRedirects(respuesta, reverse('principal'))
        self.empleado.refresh_from_db()
        self.assertEqual(self.empleado.nombre, 'Ana María')
        self.assertEqual(self.empleado.detalle.direccion, 'Coquimbo')

    def test_editar_empleado_sin_detalle_lo_crea(self):
        sin_detalle = Empleado.objects.create(rut='9.876.543-2', nombre='Pedro', apellido='Díaz', cargo='Pintor')
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('editar_empleado', args=[sin_detalle.id])).status_code, 200)
        self.client.post(reverse('editar_empleado', args=[sin_detalle.id]), self.datos(rut='9.876.543-2'))
        self.assertTrue(DetalleEmpleado.objects.filter(empleado=sin_detalle).exists())

    def test_subir_y_quitar_foto(self):
        with tempfile.TemporaryDirectory() as carpeta, override_settings(MEDIA_ROOT=carpeta):
            imagen = io.BytesIO()
            Image.new('RGB', (10, 10), 'blue').save(imagen, 'PNG')
            foto = SimpleUploadedFile('foto.png', imagen.getvalue(), content_type='image/png')

            self.client.force_login(self.admin)
            self.client.post(reverse('registrar_empleado'), self.datos(foto=foto))
            nuevo = Empleado.objects.get(nombre='Luis')
            self.assertTrue(nuevo.detalle.foto.name.startswith('images/empleados/foto'))
            self.assertContains(self.client.get(reverse('principal')), nuevo.detalle.foto.url)

            # Marcar "Limpiar" quita la foto actual
            self.client.post(reverse('editar_empleado', args=[nuevo.id]),
                             self.datos(rut=nuevo.rut, **{'foto-clear': 'on'}))
            nuevo.detalle.refresh_from_db()
            self.assertFalse(nuevo.detalle.foto)

    def test_buscar_empleado(self):
        self.client.force_login(self.admin)
        self.assertEqual(len(self.client.get(reverse('principal'), {'q': 'Rojas'}).context['empleados']), 1)
        self.assertEqual(len(self.client.get(reverse('principal'), {'q': 'Zzz'}).context['empleados']), 0)

    def test_buscar_por_nombre_completo_y_rut_sin_puntos(self):
        self.client.force_login(self.admin)
        self.assertEqual(len(self.client.get(reverse('principal'), {'q': 'Ana Rojas'}).context['empleados']), 1)
        self.assertEqual(len(self.client.get(reverse('principal'), {'q': 'Ana Soto'}).context['empleados']), 0)
        self.assertEqual(len(self.client.get(reverse('principal'), {'q': '11111111-1'}).context['empleados']), 1)

    def test_eliminar_empleado(self):
        self.client.force_login(self.admin)
        self.client.post(reverse('eliminar_empleado', args=[self.empleado.id]))
        self.assertFalse(Empleado.objects.exists())
        self.assertFalse(DetalleEmpleado.objects.exists())

    def test_no_elimina_empleado_con_asignaciones(self):
        vehiculo = Vehiculo.objects.create(marca='Suzuki', modelo='Jimny', anio=2020, patente='ABCD12')
        Asignacion.objects.create(empleado=self.empleado, vehiculo=vehiculo, motivo='Prueba de ruta')
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('eliminar_empleado', args=[self.empleado.id]), follow=True)
        self.assertContains(respuesta, 'No se puede eliminar el empleado')
        self.assertTrue(Empleado.objects.filter(id=self.empleado.id).exists())
