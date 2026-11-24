from rest_framework import serializers

from compraRepuestosApp.models import CompraRepuesto, DetalleCompra


class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = ['repuesto', 'cantidad', 'precio_unitario']


class CompraRepuestoSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(
        many=True,
        source='detalles_compra',
        required=True,
    )
    total = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CompraRepuesto
        fields = ['id', 'cliente', 'proveedor', 'fecha', 'detalles', 'total']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles_compra')
        compra = CompraRepuesto.objects.create(**validated_data)
        for detalle_data in detalles_data:
            DetalleCompra.objects.create(compra=compra, **detalle_data)
        return compra

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles_compra', None)

        instance.cliente = validated_data.get('cliente', instance.cliente)
        instance.proveedor = validated_data.get('proveedor', instance.proveedor)
        instance.save()

        if detalles_data is not None:
            instance.detalles_compra.all().delete()
            for detalle_data in detalles_data:
                DetalleCompra.objects.create(compra=instance, **detalle_data)

        return instance
