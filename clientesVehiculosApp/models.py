from django.db import models
from clientesApp.models import Cliente
from vehiculosApp.models import Vehiculo

class ClienteVehiculo(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='vehiculos_asociados',
        verbose_name='Cliente'
    )
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='duenos_asociados',
        verbose_name='Vehículo'
    )
    fecha_registro = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    observacion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Observación o Estado'
    )

    def __str__(self):
        return f'{self.cliente} -> {self.vehiculo}'

    class Meta:
        db_table = 'cliente_vehiculo'
        verbose_name = 'Relación Cliente Vehículo'
        verbose_name_plural = 'Relaciones Cliente Vehículos'