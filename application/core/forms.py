from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Carrito


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre', 'class': 'input-field'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su email', 'class': 'input-field'})
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña', 'class': 'input-field password-input'})
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme su contraseña', 'class': 'input-field password-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Usuario',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ingrese su usuario', 'class': 'input-field'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 6 caracteres.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError("El nombre no debe contener números.")
        return first_name

def carrito_count(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, comprado=False).first()
        if carrito:
            total_items = sum(item.cantidad for item in carrito.items.all())
            return {'carrito_count': total_items}
    return {'carrito_count': 0}