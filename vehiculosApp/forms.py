from django import forms
from django.utils import timezone
from vehiculosApp.estado_choices import estados
from vehiculosApp.models import Detalle, Vehiculo

class VehiculoForm(forms.ModelForm):
    marca = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Introduzca la marca del vehiculo'}
        )
    )

    modelo = forms.CharField(
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Introduzca el modelo del vehiculo'}

            )
        )

    anio = forms.IntegerField(
        required=True,
        label = 'Año',
        widget= forms.NumberInput(
            attrs={'class':'form-control'}
        )
    )

    patente = forms.CharField(
                required=True,
                widget=forms.TextInput(
                    attrs={'class': 'form-control',
                           'placeholder': 'Introduzca la patente del vehiculo'}
    
                )
            )

    imagen = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean_anio(self):
        anio = self.cleaned_data.get('anio')
        anio_actual = timezone.now().year

        if anio and (anio < 1886 or anio > anio_actual):
            raise forms.ValidationError(f"El año debe estar entre 1886 y {anio_actual}.")

        if anio > anio_actual:
            raise forms.ValidationError(f"El año no puede ser mayor al año actual ({anio_actual}).")
        return anio

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')
        if patente:
            if len(patente) !=6:
                raise forms.ValidationError("La patente debe tener entre 6 caracteres.")
        return patente

    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'anio', 'patente', 'imagen']


class DetalleForm(forms.ModelForm):
    color = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Introduzca el color del vehiculo'}
        )
    )

    tipo_motor = forms.CharField(
        required=True,
            widget=forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Introduzca el tipo de motor del vehiculo'}

            )
        )

    tipo_caja = forms.CharField(
        required=True,
                widget=forms.TextInput(
                    attrs={'class': 'form-control',
                           'placeholder': 'Introduzca el tipo de caja del vehiculo'}
    
                )
            )

    fecha_ultimo_servicio = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={'class':'form-select'}
        )
    )

    kilometraje = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={'class':'form-select'}
        )
    )

    estado = forms.ChoiceField(
        required=True,
        choices=estados,
        widget=forms.Select(attrs={'class':'form-select'})
    )

    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 4,
                   'placeholder': 'Ingrese observaciones adicionales (opcional)'}
        )
    )

    def clean_fecha_ultimo_servicio(self):
    
            ultimoservicio = self.cleaned_data.get('fecha_ultimo_servicio')
            fecha_maxima = timezone.now().date()  # Obtener la fecha actual
    
            if ultimoservicio and ultimoservicio > fecha_maxima:
                raise forms.ValidationError("La fecha del último servicio no puede ser mayor a la fecha actual.")

            if not ultimoservicio:
                raise forms.ValidationError("La fecha del último servicio es obligatoria.")
    
            return ultimoservicio

    class Meta:
        model = Detalle
        fields = ['color', 'tipo_motor', 'tipo_caja', 'fecha_ultimo_servicio', 'kilometraje', 'estado', 'observaciones']

    

detalle_formset = forms.inlineformset_factory(
    Vehiculo,
    Detalle,
    form=DetalleForm,)

