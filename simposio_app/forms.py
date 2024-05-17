# simposio_app/forms.py

from django import forms
from .models import Estudiante, Expositor


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombres', 'apellidos', 'carnet', 'correo_electronico', 'telefono', 'edad',
                  'semestre_o_ciclo', 'boleta_de_pago', 'numero_de_boleta', 'talla_de_camiseta']


class ExpositorForm(forms.ModelForm):
    class Meta:
        model = Expositor
        fields = ['nombres', 'apellidos', 'correo_electronico',
                  'telefono', 'especialidad', 'institucion', 'tema_a_impartir']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'apellidos': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-input', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'especialidad': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'institucion': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'tema_a_impartir': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
        }
