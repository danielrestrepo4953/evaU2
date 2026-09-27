from django.db import models
from django.utils import timezone

# Create your models here.
class repuestos(models.Model):
    codigo = models.CharField(max_length=10, verbose_name='codigo de los repuestos')
    nombre = models.CharField(max_length=100, verbose_name='nombre de los repuestos')
    precio = models.PositiveIntegerField(verbose_name='precio de los repuestos')
    stock = models.IntegerField(default=0, verbose_name='stock de los repuestos')
    detalle = models.CharField(max_length=200, verbose_name='detalle de los repuestos')
    imagen = models.ImageField(upload_to='images/repuestos/')
    creado = models.DateTimeField(default=timezone.now, verbose_name='fecha de creacion')

    def __str__(self):
        return f"{self.nombre} {self.codigo} {self.precio} {self.stock} {self.detalle}"

    class Meta:
        db_table = 'repuestos'
        verbose_name = 'repuesto'
        verbose_name_plural = 'repuestos'
        ordering = ['nombre', 'precio']

class descripcion (models.Model):
    repuesto = models.ForeignKey(repuestos, on_delete=models.CASCADE, verbose_name='repuesto')
    descripcion = models.TextField(verbose_name='descripcion del repuesto')

    def __str__(self):
        return f"{self.repuesto.nombre} {self.descripcion}"

    class Meta:
        db_table = 'descripcion'
        verbose_name = 'descripcion'
        verbose_name_plural = 'descripciones'
        ordering = ['repuesto']
