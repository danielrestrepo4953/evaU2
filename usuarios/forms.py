from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

User = get_user_model()


class UsuarioCreationForm(UserCreationForm):
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label='Cuenta activa',
    )

    grupo = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        label='Grupo',
        empty_label='Seleccione un grupo',
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Ya existe un usuario registrado con este correo.'
            )

        return email

    



    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_active",
        )

class UsuarioUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        required=False,
        label="Nueva contraseña",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(    
        required=False,
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput,
    )

    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        empty_label="Seleccione un grupo",
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        usuario_existente = User.objects.filter(
            email__iexact=email
        ).exclude(pk=self.instance.pk).exists()

        if usuario_existente:
            raise forms.ValidationError(
                'Ya existe otro usuario registrado con este correo.'
            )

        return email

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

        if self.instance and self.instance.pk:
            self.fields["password1"].required = False
            self.fields["password2"].required = False
            self.fields["password1"].label = "Nueva contraseña"
            self.fields["password2"].label = "Confirmar nueva contraseña"

        if self.instance.pk:
            self.fields["grupo"].initial = self.instance.groups.first()

    def save(self, commit=True):
        """Guarda el usuario y asigna el grupo."""
        contraseña_actual = self.instance.password
        """Guarda el usuario y asigna el grupo."""
        usuario = super().save(commit=False)

        if (
            self.instance.pk
            and not self.cleaned_data.get("password1")
            and not self.cleaned_data.get("password2")
        ):
            usuario.password = contraseña_actual

        if self.cleaned_data.get("password1") and self.cleaned_data.get("password2"):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            usuario.set_password(self.cleaned_data["password1"])

        if commit:
            usuario.save()
            usuario.groups.set([self.cleaned_data["grupo"]])

        return usuario