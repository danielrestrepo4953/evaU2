import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from asignacionesApp.models import Asignacion
from empleadosApp.models import Empleado
from vehiculosApp.models import Vehiculo


class AsignacionesTests(TestCase):

    def setUp(self):
        User = get_user_model()
        permisos = Permission.objects.filter(content_type__app_label='asignacionesApp')

        self.admin = User.objects.create_user('admin_test', password='clave-test-123')
        self.admin.user_permissions.set(permisos)

        self.solo_lectura = User.objects.create_user('lector_test', password='clave-test-123')
        self.solo_lectura.user_permissions.add(permisos.get(codename='view_asignacion'))

        self.empleado = Empleado.objects.create(rut='11111111-1', nombre='Ana', apellido='Rojas', cargo='Mecánico')
        self.empleado2 = Empleado.objects.create(rut='22222222-2', nombre='Luis', apellido='Soto', cargo='Chofer')
        self.vehiculo = Vehiculo.objects.create(marca='Suzuki', modelo='Jimny', anio=2020, patente='ABCD12')

    def datos(self, **cambios):
        datos = {
            'empleado': self.empleado.id,
            'vehiculo': self.vehiculo.id,
            'fecha_inicio': '2026-10-01',
            'fecha_fin': '',
            'motivo': 'Prueba de ruta',
            'estado': 'Activa',
        }
        datos.update(cambios)
        return datos

    def test_sin_login_redirige_al_login(self):
        respuesta = self.client.get(reverse('inicio_asignaciones'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/login/', respuesta.url)

    def test_usuario_sin_permiso_de_crear_recibe_403(self):
        self.client.force_login(self.solo_lectura)
        self.assertEqual(self.client.get(reverse('inicio_asignaciones')).status_code, 200)
        self.assertEqual(self.client.get(reverse('registrar_asignacion')).status_code, 403)

    def test_registrar_asignacion(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('registrar_asignacion'), self.datos())
        self.assertRedirects(respuesta, reverse('inicio_asignaciones'))
        self.assertEqual(Asignacion.objects.count(), 1)

    def test_vehiculo_no_puede_tener_dos_asignaciones_activas(self):
        Asignacion.objects.create(empleado=self.empleado, vehiculo=self.vehiculo, motivo='Primera asignación')
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('registrar_asignacion'), self.datos(empleado=self.empleado2.id))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Este vehículo ya está asignado')
        self.assertEqual(Asignacion.objects.count(), 1)

    def test_fecha_fin_no_puede_ser_anterior_al_inicio(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('registrar_asignacion'),
                                     self.datos(fecha_fin='2026-09-01', estado='Finalizada'))
        self.assertContains(respuesta, 'no puede ser anterior')
        self.assertEqual(Asignacion.objects.count(), 0)

    def test_finalizada_exige_fecha_fin(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('registrar_asignacion'), self.datos(estado='Finalizada'))
        self.assertContains(respuesta, 'debes indicar la fecha de término')

    def test_editar_asignacion(self):
        asignacion = Asignacion.objects.create(empleado=self.empleado, vehiculo=self.vehiculo, motivo='Prueba de ruta')
        self.client.force_login(self.admin)
        self.client.post(reverse('editar_asignacion', args=[asignacion.id]),
                         self.datos(estado='Finalizada', fecha_fin='2026-10-05'))
        asignacion.refresh_from_db()
        self.assertEqual(asignacion.estado, 'Finalizada')
        self.assertEqual(asignacion.fecha_fin, datetime.date(2026, 10, 5))

    def test_buscar_por_patente(self):
        Asignacion.objects.create(empleado=self.empleado, vehiculo=self.vehiculo, motivo='Prueba de ruta')
        self.client.force_login(self.admin)
        encontrada = self.client.get(reverse('inicio_asignaciones'), {'q': 'ABCD'})
        no_encontrada = self.client.get(reverse('inicio_asignaciones'), {'q': 'ZZZZ'})
        self.assertEqual(len(encontrada.context['asignaciones']), 1)
        self.assertEqual(len(no_encontrada.context['asignaciones']), 0)

    def test_eliminar_asignacion(self):
        asignacion = Asignacion.objects.create(empleado=self.empleado, vehiculo=self.vehiculo, motivo='Prueba de ruta')
        self.client.force_login(self.admin)
        self.client.post(reverse('eliminar_asignacion', args=[asignacion.id]))
        self.assertFalse(Asignacion.objects.exists())

    def test_comando_asigna_permisos_por_grupo(self):
        from django.core.management import call_command
        call_command('permisos_asignaciones', stdout=open(__import__('os').devnull, 'w'))
        self.assertEqual(Group.objects.get(name='Administrador').permissions.count(), 4)
        self.assertEqual(Group.objects.get(name='Supervisor').permissions.count(), 3)
        self.assertEqual(Group.objects.get(name='Empleado').permissions.count(), 1)
