from django import forms
from .models import Salon

class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ['nombre', 'descripcion', 'capacidad_maxima', 'precio_base', 'adicionales_disponibles', 'imagen_portada']
        
        # Le inyectamos las clases de Bootstrap directamente desde Python
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ej: Salón Esmeralda'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describí las características del lugar...'}),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'imagen_portada': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
            # Para los checkbox de los extras, Django usa SelectMultiple, lo estilizamos un poco
            'adicionales_disponibles': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input ms-2 mb-2'}),
        }