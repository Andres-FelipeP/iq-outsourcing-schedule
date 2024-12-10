from django import forms
from .models import User, Reserva
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nombre', 'email', 'cedula', 'apellido1', 'apellido2', 'tipo_usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control bg-dark-subtle'}),
            'apellido1': forms.TextInput(attrs={'class': 'form-control bg-dark-subtle'}),
            'apellido2': forms.TextInput(attrs={'class': 'form-control bg-dark-subtle'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark-subtle'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control bg-dark-subtle'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control bg-dark-subtle'}),

        }


class LoginForm(forms.Form):
    cedula = forms.CharField(max_length=150, label='Cedula' )
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['cedula', 'nombre', 'apellido1', 'apellido2', 'email', 'tipo_usuario']  # Los campos que quieres editar

        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido1': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'turno']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}),
        }