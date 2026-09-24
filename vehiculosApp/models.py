from django.db import models
from django.utils import timezone
from vehiculosApp.estado_choices import estados
# Create your models here.
class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.IntegerField(verbose_name="Año de fabricación")
    patente = models.CharField(max_length=10, unique=True)
    imagen = models.ImageField(upload_to='images/vehiculos/', null=True, blank=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"

    class Meta:
        db_table = "vehiculos"
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['marca', 'modelo', 'anio']

class Detalle(models.Model):
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE, related_name='detalle')
    color = models.CharField(max_length=50)
    tipo_motor = models.CharField(max_length=50)
    tipo_caja = models.CharField(max_length=50)
    fecha_ultimo_servicio = models.DateField(default=timezone.now, blank=True, null=True)
    kilometraje = models.IntegerField()
    estado = models.CharField(max_length=50, choices=estados, verbose_name="Estado del vehículo")
    observaciones = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Detalle de {self.vehiculo.marca} {self.vehiculo.modelo} ({self.vehiculo.anio})"

    class Meta:
        db_table = "detalles_vehiculos"
        verbose_name = "Detalle del Vehículo"
        verbose_name_plural = "Detalles de Vehículos"
        ordering = ['vehiculo__marca', 'vehiculo__modelo', 'vehiculo__anio']
