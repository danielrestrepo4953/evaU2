from django import forms
from django.forms import inlineformset_factory

from reparacionesApp.models import Reparacion, RepuestoUtilizado


class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ['vehiculo', 'detalle']
        widgets = {
            'vehiculo' : forms.Select(attrs={'class' : 'form-select',}),
            'detalle' : forms.Textarea(attrs={'class' : 'form-control',
                                              'rows' : 4,
                                              'placeholder' : 'Describe el trabajo realizado', })
        }


class RepuestoUtilizadoForm(forms.ModelForm):
    class Meta:
        model = RepuestoUtilizado
        fields = ['repuesto', 'cantidad']
        widgets = {
            'repuesto' : forms.Select(attrs={
                'class' : 'form-select repuesto-select', 
            }),
            'cantidad' : forms.NumberInput(attrs={
                'class': 'form-control cantidad-input', 
                'min':1,}),


            
        }

RepuestoUtilizadoFormSet = inlineformset_factory(
    Reparacion,
    RepuestoUtilizado,
    form = RepuestoUtilizadoForm,
    extra = 1,
    can_delete= True
)
