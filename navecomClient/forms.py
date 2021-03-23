from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import *

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)


    class Meta:
        model = usuario
        fields = ('email', 'password','tipo_usuario','no_documento', 'nombre', 'apellido', 'no_celular', 'tel_fijo','direccion', 'barrio', 'referencia_vivienda', 'nickname', 'estado','usuario_administrador', 'groups')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()

        if user.tipo_usuario.id_ty_us == 2 or user.tipo_usuario.id_ty_us == 1:
            user.usuario_administrador = True
            user.save()
            
        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = usuario
        fields = ('email', 'password','tipo_usuario','no_documento', 'nombre', 'apellido', 'no_celular', 'tel_fijo','direccion', 'barrio', 'referencia_vivienda', 'nickname', 'estado', 'groups')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
"""
class factureAddForm(forms.ModelForm):

    class Meta:

        model = facturas
        fields = ('id_bill' , 'pago', 'total_pagar', 'total_recibido', 'total_devuelto', 'fecha_pago',
            'fecha_limite_pago', 'metodo_pago', 'codigo_convenio', 'codigo_epy', 'pin_epy', 'numero_recibo')

"""