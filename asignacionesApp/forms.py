from django import forms

from asignacionesApp.models import Asignacion


class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['empleado', 'vehiculo', 'fecha_inicio', 'fecha_fin', 'motivo', 'estado']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control',
                                            'rows': 3,
                                            'placeholder': 'Ej: Prueba de ruta después de la reparación'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_motivo(self):
        motivo = (self.cleaned_data.get('motivo') or '').strip()
        if len(motivo) < 5:
            raise forms.ValidationError("El motivo debe tener al menos 5 caracteres.")
        return motivo

    def clean(self):
        cleaned_data = super().clean()
        vehiculo = cleaned_data.get('vehiculo')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        estado = cleaned_data.get('estado')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_fin', "La fecha de término no puede ser anterior a la fecha de inicio.")

        if estado == Asignacion.FINALIZADA and not fecha_fin:
            self.add_error('fecha_fin', "Para finalizar una asignación debes indicar la fecha de término.")

        # Un vehículo solo puede estar asignado a un empleado a la vez
        if estado == Asignacion.ACTIVA and vehiculo:
            ocupado = (Asignacion.objects
                       .filter(vehiculo=vehiculo, estado=Asignacion.ACTIVA)
                       .exclude(pk=self.instance.pk)
                       .select_related('empleado')
                       .first())
            if ocupado:
                self.add_error('vehiculo', f"Este vehículo ya está asignado a {ocupado.empleado} "
                                           f"(asignación #{ocupado.id}). Finaliza esa asignación primero.")

        return cleaned_data
