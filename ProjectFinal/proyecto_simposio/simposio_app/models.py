# simposio_app/models.py
from django.db import models


class Estudiante(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    carnet = models.CharField(max_length=20, unique=True)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    edad = models.PositiveIntegerField()
    fecha_nacimiento = models.DateField()
    semestre_o_ciclo = models.CharField(max_length=50)
    boleta_de_pago = models.ImageField(upload_to='boletas_de_pago/')
    talla_de_camiseta = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Expositor(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    tema_a_impartir = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Pago(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    codigo_boleta = models.CharField(max_length=100)
    fecha_pago = models.DateField(auto_now_add=True)
