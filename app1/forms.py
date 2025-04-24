from django import forms
from .models import Zapato, Cliente, Orden

class ZapatoForm(forms.ModelForm):
    class Meta:
        model = Zapato
        fields = ['referencia', 'modelo', 'talla', 'sexo', 'color', 'requerimientos', 'observaciones']
        widgets = {
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Referencia'}),
            'modelo': forms.Select(attrs={'class': 'form-control'}),
            'talla': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'requerimientos': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Requerimientos'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
        }
        