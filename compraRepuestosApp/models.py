from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from repuestosApp.models import repuestos
from clientesApp.models import Cliente


class CompraRepuesto(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,
        related_name='compras',
        verbose_name='Cliente'
    )
    proveedor = models.CharField(max_length=100, verbose_name='Proveedor')
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha de compra')
    repuestos = models.ManyToManyField(
        repuestos,
        through='DetalleCompra',
        related_name='compras',
        blank=True,
        verbose_name='Repuestos'
    )

    def __str__(self):
        return f'{self.proveedor} - {self.fecha}'

    @property
    def total(self):
        return sum((item.subtotal for item in self.detalles_compra.all()), Decimal('0.00'))

    class Meta:
        db_table = 'compra_repuesto'
        verbose_name = 'Compra de repuestos'
        verbose_name_plural = 'Compras de repuestos'


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        CompraRepuesto,
        on_delete=models.CASCADE,
        related_name='detalles_compra'
    )
    repuesto = models.ForeignKey(
        repuestos,
        on_delete=models.PROTECT,
        related_name='usos_en_compras'
    )
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio unitario',
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def __str__(self):
        return f'{self.cantidad} x {self.repuesto} en {self.compra}'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    class Meta:
        unique_together = ('compra', 'repuesto')
        constraints = [
            models.CheckConstraint(condition=models.Q(cantidad__gte=1), name='compra_cantidad_positiva'),
            models.CheckConstraint(condition=models.Q(precio_unitario__gte=0), name='compra_precio_no_negativo'),
        ]
        db_table = 'detalle_compra'
        verbose_name = 'Detalle de compra'
        verbose_name_plural = 'Detalles de compra'
