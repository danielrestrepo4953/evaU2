from django import forms


class SolicitarRecuperacionForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'email',
                'placeholder': 'correo@ejemplo.com',
            }
        ),
    )

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()