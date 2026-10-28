from django.db import models
from django.utils import timezone
from empleadosApp.models import Empleado
from vehiculosApp.models import Vehiculo


class Asignacion(models.Model):
    ACTIVA = 'Activa'
    FINALIZADA = 'Finalizada'
    ESTADOS = [
        (ACTIVA, 'Activa'),
        (FINALIZADA, 'Finalizada'),
    ]

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.RESTRICT,
        related_name='asignaciones',
        verbose_name='Empleado'
    )
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.RESTRICT,
        related_name='asignaciones',
        verbose_name='Vehículo'
    )
    fecha_inicio = models.DateField(default=timezone.localdate, verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fecha de término')
    motivo = models.CharField(max_length=255, verbose_name='Motivo de la asignación')
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ACTIVA, verbose_name='Estado')
    creado = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')

    def __str__(self):
        return f'{self.empleado} - {self.vehiculo}'

    class Meta:
        db_table = 'asignaciones'
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'
        ordering = ['-fecha_inicio', '-id']
