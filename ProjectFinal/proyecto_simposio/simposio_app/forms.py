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
        fields = '__all__'
