from rest_framework import serializers
from .models import Estudiante, Expositor, Pago

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

class ExpositorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expositor
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'
