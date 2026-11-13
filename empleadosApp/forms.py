import re

from django import forms
from django.db.models import Value
from django.db.models.functions import Replace, Upper
from django.utils import timezone

from empleadosApp.models import Empleado, DetalleEmpleado

PATRON_RUT = re.compile(r'^(\d{1,2})\.?(\d{3})\.?(\d{3})-?([\dkK])$')
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]+$")


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['rut', 'nombre', 'apellido', 'cargo']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduzca el nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduzca el apellido'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mecánico'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut', '').strip().replace(' ', '')
        coincidencia = PATRON_RUT.match(rut)
        if not coincidencia:
            raise forms.ValidationError("El RUT debe tener el formato 12.345.678-9 (o 12345678-9).")

        # Se guarda siempre con el mismo formato para que no se repitan RUT escritos distinto
        millones, miles, unidades, dv = coincidencia.groups()
        rut_normalizado = f"{millones}.{miles}.{unidades}-{dv.upper()}"

        # Los empleados antiguos pueden tener el RUT guardado sin puntos, por eso se compara sin ellos
        repetido = (Empleado.objects
                    .annotate(rut_sin_puntos=Upper(Replace('rut', Value('.'), Value(''))))
                    .filter(rut_sin_puntos=rut_normalizado.replace('.', ''))
                    .exclude(pk=self.instance.pk)
                    .exists())
        if repetido:
            raise forms.ValidationError("Ya existe un empleado registrado con este RUT.")

        return rut_normalizado

    def validar_nombre(self, campo, etiqueta):
        valor = self.cleaned_data.get(campo, '').strip()
        if len(valor) < 2:
            raise forms.ValidationError(f"El {etiqueta} debe tener al menos 2 caracteres.")
        if not PATRON_NOMBRE.match(valor):
            raise forms.ValidationError(f"El {etiqueta} solo puede contener letras y espacios.")
        return valor

    def clean_nombre(self):
        return self.validar_nombre('nombre', 'nombre')

    def clean_apellido(self):
        return self.validar_nombre('apellido', 'apellido')

    def clean_cargo(self):
        cargo = self.cleaned_data.get('cargo', '').strip()
        if len(cargo) < 3:
            raise forms.ValidationError("El cargo debe tener al menos 3 caracteres.")
        return cargo


class DetalleEmpleadoForm(forms.ModelForm):
    class Meta:
        model = DetalleEmpleado
        fields = ['foto', 'direccion', 'fecha_contratacion', 'telefono', 'correo']
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduzca la dirección'}),
            'fecha_contratacion': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +56 9 1234 5678'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: nombre@empresa.cl'}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not re.fullmatch(r'\+?[\d ]+', telefono):
            raise forms.ValidationError("El teléfono solo puede contener números, espacios y el signo +.")
        digitos = re.sub(r'\D', '', telefono)
        if not 8 <= len(digitos) <= 12:
            raise forms.ValidationError("El teléfono debe tener entre 8 y 12 dígitos.")
        return telefono

    def clean_fecha_contratacion(self):
        fecha = self.cleaned_data.get('fecha_contratacion')
        if fecha and fecha > timezone.localdate():
            raise forms.ValidationError("La fecha de contratación no puede ser mayor a la fecha actual.")
        return fecha
