from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import Permission, User
from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse

from clientesApp.models import Cliente
from repuestosApp.models import repuestos
from .models import CompraRepuesto, DetalleCompra


class CompraTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='comprador', password='test-password')
        cls.user.user_permissions.add(*Permission.objects.filter(
            content_type__app_label='compraRepuestosApp',
            codename__in=['view_comprarepuesto', 'add_comprarepuesto', 'add_detallecompra'],
        ))
        cls.cliente = Cliente.objects.create(nombre='Cliente de prueba')
        cls.repuesto = repuestos.objects.create(
            codigo='TEST', nombre='Filtro', precio=100, stock=10, detalle='Prueba',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def datos(self, cantidad=3, precio='100.25', filas=1):
        data = {'cliente': self.cliente.pk, 'proveedor': 'Proveedor',
                'detalles_compra-TOTAL_FORMS': filas, 'detalles_compra-INITIAL_FORMS': 0}
        for i in range(filas):
            data.update({f'detalles_compra-{i}-repuesto': self.repuesto.pk,
                         f'detalles_compra-{i}-cantidad': cantidad,
                         f'detalles_compra-{i}-precio_unitario': precio})
        return data

    def test_registro_actualiza_stock_y_total(self):
        response = self.client.post(reverse('registrar_compra'), self.datos())
        self.assertRedirects(response, reverse('inicio_compras'))
        self.repuesto.refresh_from_db()
        self.assertEqual(self.repuesto.stock, 13)
        self.assertEqual(CompraRepuesto.objects.get().total, Decimal('300.75'))
        self.assertEqual(DetalleCompra.objects.count(), 1)

    def test_rechaza_compra_sin_detalles(self):
        response = self.client.post(reverse('registrar_compra'), self.datos(filas=0))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['formset'].non_form_errors())
        self.assertFalse(CompraRepuesto.objects.exists())

    def test_rechaza_valores_invalidos(self):
        for cantidad, precio in [(0, '10'), (-1, '10'), (1, '-10')]:
            with self.subTest(cantidad=cantidad, precio=precio):
                response = self.client.post(reverse('registrar_compra'), self.datos(cantidad, precio))
                self.assertEqual(response.status_code, 200)
                self.assertFalse(CompraRepuesto.objects.exists())
        self.repuesto.refresh_from_db()
        self.assertEqual(self.repuesto.stock, 10)

    def test_rechaza_repuesto_duplicado(self):
        response = self.client.post(reverse('registrar_compra'), self.datos(filas=2))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CompraRepuesto.objects.exists())

    def test_rechaza_todos_los_detalles_eliminados(self):
        data = self.datos()
        data['detalles_compra-0-DELETE'] = 'on'
        self.client.post(reverse('registrar_compra'), data)
        self.assertFalse(CompraRepuesto.objects.exists())

    def test_error_stock_revierte_compra(self):
        with patch('django.db.models.query.QuerySet.update', side_effect=DatabaseError('Prueba')):
            with self.assertRaises(DatabaseError):
                self.client.post(reverse('registrar_compra'), self.datos())
        self.assertFalse(CompraRepuesto.objects.exists())
        self.assertFalse(DetalleCompra.objects.exists())
        self.repuesto.refresh_from_db()
        self.assertEqual(self.repuesto.stock, 10)

    def test_exige_autenticacion_y_permisos(self):
        self.client.logout()
        for name in ['inicio_compras', 'registrar_compra']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 302)
        user = User.objects.create_user(username='sin_permisos')
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('inicio_compras')).status_code, 403)
        self.assertEqual(self.client.post(reverse('registrar_compra'), self.datos()).status_code, 403)
        self.assertFalse(CompraRepuesto.objects.exists())

    def test_formulario_y_menu_renderizan(self):
        self.assertContains(self.client.get(reverse('registrar_compra')), 'Agregar repuesto')
        self.assertContains(self.client.get(reverse('menu-principal')), 'Menú principal')

    def test_listado_precarga_relaciones(self):
        for _ in range(3):
            compra = CompraRepuesto.objects.create(cliente=self.cliente, proveedor='Proveedor')
            DetalleCompra.objects.create(compra=compra, repuesto=self.repuesto,
                                         cantidad=2, precio_unitario='100.25')
        response = self.client.get(reverse('inicio_compras'))
        with self.assertNumQueries(0):
            for compra in response.context['compras']:
                self.assertEqual(compra.total, Decimal('200.50'))
                str(compra.cliente)
                for detalle in compra.detalles_compra.all():
                    str(detalle.repuesto)

    def test_acceso_directo_protegido_en_todas_las_rutas(self):
        rutas = ['/compras/', '/compras/registrar/',
                 '/compra-repuestos/', '/compra-repuestos/registrar/']
        self.client.logout()
        for ruta in rutas:
            for metodo in ['get', 'post']:
                with self.subTest(ruta=ruta, metodo=metodo, usuario='anonimo'):
                    response = getattr(self.client, metodo)(ruta, self.datos() if metodo == 'post' else {})
                    self.assertRedirects(response, '/usuarios/login/?next=' + ruta,
                                         fetch_redirect_response=False)
        user = User.objects.create_user(username='sin_acceso_directo')
        self.client.force_login(user)
        for ruta in rutas:
            for metodo in ['get', 'post']:
                with self.subTest(ruta=ruta, metodo=metodo, usuario='sin_permiso'):
                    response = getattr(self.client, metodo)(ruta, self.datos() if metodo == 'post' else {})
                    self.assertEqual(response.status_code, 403)
        self.assertFalse(CompraRepuesto.objects.exists())
        self.assertFalse(DetalleCompra.objects.exists())
        self.repuesto.refresh_from_db()
        self.assertEqual(self.repuesto.stock, 10)

    def test_permiso_de_consulta_no_permite_registrar(self):
        user = User.objects.create_user(username='solo_consulta')
        user.user_permissions.add(Permission.objects.get(
            content_type__app_label='compraRepuestosApp', codename='view_comprarepuesto'))
        self.client.force_login(user)
        for listado, registro in [('/compras/', '/compras/registrar/'),
                                  ('/compra-repuestos/', '/compra-repuestos/registrar/')]:
            with self.subTest(registro=registro):
                self.assertEqual(self.client.get(listado).status_code, 200)
                self.assertEqual(self.client.get(registro).status_code, 403)
                self.assertEqual(self.client.post(registro, self.datos()).status_code, 403)
        self.assertFalse(CompraRepuesto.objects.exists())
        self.assertFalse(DetalleCompra.objects.exists())
        self.repuesto.refresh_from_db()
        self.assertEqual(self.repuesto.stock, 10)
