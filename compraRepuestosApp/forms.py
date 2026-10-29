from django import forms
from django.forms import inlineformset_factory

from compraRepuestosApp.models import CompraRepuesto, DetalleCompra


class CompraRepuestoForm(forms.ModelForm):
    class Meta:
        model = CompraRepuesto
        fields = ['cliente', 'proveedor']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
            }),
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proveedor',
            }),
        }


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['repuesto', 'cantidad', 'precio_unitario']
        widgets = {
            'repuesto': forms.Select(attrs={
                'class': 'form-select repuesto-select',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control cantidad-input',
                'min': 1,
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control precio-input',
                'min': 0,
                'step': '0.01',
            }),
        }


DetalleCompraFormSet = inlineformset_factory(
    CompraRepuesto,
    DetalleCompra,
    form=DetalleCompraForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True
)
