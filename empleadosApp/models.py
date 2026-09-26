from django.db import models
from django.utils import timezone
# Create your models here.
class Empleado(models.Model):
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        db_table = "empleados"
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ["apellido", "nombre"]
        
class DetalleEmpleado(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, related_name='detalle', verbose_name="Empleado")
    foto = models.ImageField(upload_to='images/empleados/', null=True, blank=True, verbose_name="Foto")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    fecha_contratacion = models.DateField(null=True, blank=True, verbose_name="Fecha de Contratación")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    correo = models.EmailField(max_length=100, verbose_name="Correo")
    creado = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    
    def __str__(self):
        return f"Detalle de {self.empleado.nombre} {self.empleado.apellido}"

    class Meta:
        db_table = "detalle_empleados"
        verbose_name = "Detalle de Empleado"
        verbose_name_plural = "Detalles de Empleados"
        ordering = ["empleado__apellido", "empleado__nombre"]