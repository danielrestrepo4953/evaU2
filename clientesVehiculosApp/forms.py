from django import forms
from clientesVehiculosApp.models import ClienteVehiculo

class ClienteVehiculoForm(forms.ModelForm):
    class Meta:
        model = ClienteVehiculo
        fields = ['cliente', 'vehiculo', 'observacion']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej. Vehículo principal / Uso familiar'}
            ),
        }