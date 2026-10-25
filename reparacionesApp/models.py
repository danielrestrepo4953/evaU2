from django.db import models
from vehiculosApp.models import Vehiculo
from repuestosApp.models import repuestos


class Reparacion(models.Model):
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.RESTRICT,
        related_name='reparaciones',
        verbose_name='Vehículo'
    )
    detalle = models.CharField(
        max_length=255,
        verbose_name='Detalle de reparación'
    )
    fecha = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de reparación'
    )
    repuestos = models.ManyToManyField(
        repuestos,
        through='RepuestoUtilizado',
        related_name='reparaciones',
        blank=True,
        verbose_name='Repuestos'
    )

    def __str__(self):
        return f'{self.vehiculo} - {self.detalle}'

    class Meta:
        db_table = 'reparacion'
        verbose_name = 'Reparación'
        verbose_name_plural = 'Reparaciones'


class RepuestoUtilizado(models.Model):
    reparacion = models.ForeignKey(
        Reparacion,
        on_delete=models.CASCADE,
        related_name='repuestos_utilizados'
    )
    repuesto = models.ForeignKey(
        repuestos,
        on_delete=models.PROTECT,
        related_name='usos_en_reparaciones'
    )
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.repuesto} en {self.reparacion}'

    class Meta:
        unique_together = ('reparacion', 'repuesto')
        db_table = 'repuesto_utilizado'
        verbose_name = 'Repuesto Utilizado'
        verbose_name_plural = 'Repuestos Utilizados'