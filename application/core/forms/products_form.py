from django import forms
from application.core.models import Producto
from django.core.exceptions import ValidationError
import unicodedata

def normalizar_texto(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto.lower())
        if not unicodedata.combining(c)
    ).strip()

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'marca', 'descripcion', 'cantidad', 'precio', 'imagen', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Nombre del producto'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'marca': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'Descripción del producto'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Cantidad disponible'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Precio del producto'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'w-full text-gray-700 bg-white border border-gray-300 rounded-xl file:bg-indigo-600 file:text-white file:px-4 file:py-2 file:rounded file:cursor-pointer'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-checkbox text-indigo-600 rounded focus:ring-indigo-500'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        marca = cleaned_data.get("marca")

        if nombre and marca:
            nombre_normalizado = normalizar_texto(nombre)

            # Filtrar productos que coincidan en nombre y marca
            productos_existentes = Producto.objects.filter(
                marca=marca
            )

            # Excluir este producto si está siendo editado
            if self.instance.pk:
                productos_existentes = productos_existentes.exclude(pk=self.instance.pk)

            # Validar por coincidencia del nombre normalizado
            for producto in productos_existentes:
                if normalizar_texto(producto.nombre) == nombre_normalizado:
                    raise ValidationError("Ya existe un producto con ese nombre y marca.")

        return cleaned_data
