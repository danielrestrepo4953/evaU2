import re

from rest_framework import serializers

from empleadosApp.models import Empleado, DetalleEmpleado

PATRON_RUT = re.compile(r'^\d{1,2}\.?\d{3}\.?\d{3}-?[\dkK]$')
PATRON_TELEFONO = re.compile(r'^\+?[\d ]+$')


class DetalleEmpleadoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleEmpleado
        fields = ['foto', 'direccion', 'fecha_contratacion', 'telefono', 'correo']

    def validate_telefono(self, value):
        value = value.strip()
        if not PATRON_TELEFONO.fullmatch(value):
            raise serializers.ValidationError(
                'El teléfono solo puede contener números, espacios y el signo +.'
            )
        digitos = re.sub(r'\D', '', value)
        if not 8 <= len(digitos) <= 12:
            raise serializers.ValidationError(
                'El teléfono debe tener entre 8 y 12 dígitos.'
            )
        return value


class EmpleadoPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id', 'rut', 'nombre', 'apellido', 'cargo']


class EmpleadoAdminSerializer(serializers.ModelSerializer):
    detalle = DetalleEmpleadoAdminSerializer(required=False)

    class Meta:
        model = Empleado
        fields = ['id', 'rut', 'nombre', 'apellido', 'cargo', 'detalle']

    def validate_rut(self, value):
        value = value.strip().replace(' ', '')
        if not PATRON_RUT.fullmatch(value):
            raise serializers.ValidationError(
                'El RUT debe tener el formato 12.345.678-9.'
            )
        repetido = (
            Empleado.objects.filter(rut=value)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        )
        if repetido:
            raise serializers.ValidationError(
                'Ya existe un empleado registrado con este RUT.'
            )
        return value

    def create(self, validated_data):
        detalle_data = validated_data.pop('detalle', None)
        empleado = Empleado.objects.create(**validated_data)
        if detalle_data:
            DetalleEmpleado.objects.create(empleado=empleado, **detalle_data)
        return empleado

    def update(self, instance, validated_data):
        detalle_data = validated_data.pop('detalle', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if detalle_data is not None:
            detalle, _ = DetalleEmpleado.objects.get_or_create(empleado=instance)
            for attr, value in detalle_data.items():
                setattr(detalle, attr, value)
            detalle.save()

        return instance
