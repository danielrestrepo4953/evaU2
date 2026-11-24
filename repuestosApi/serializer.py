from rest_framework import serializers
from repuestosApp.models import repuestos


class RepuestoPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = repuestos
        fields = ['codigo', 'nombre', 'precio', 'stock']


class RepuestoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = repuestos
        fields = ['codigo', 'nombre', 'detalle', 'precio', 'stock', 'imagen']
