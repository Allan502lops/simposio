# simposio_app/forms.py

from django import forms
from .models import Estudiante, Expositor

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'

class ExpositorForm(forms.ModelForm):
    class Meta:
        model = Expositor
        fields = '__all__'
