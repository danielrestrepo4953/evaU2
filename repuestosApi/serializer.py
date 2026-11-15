from rest_framework import serializers
from repuestosApp.models import repuestos

class RepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = repuestos
        fields = ['codigo', 'nombre', 'detalle', 'precio', 'stock']