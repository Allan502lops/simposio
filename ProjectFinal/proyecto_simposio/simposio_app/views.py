# simposio_app/views.py

import qrcode
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import EstudianteForm, ExpositorForm  # Importar ambos formularios
from .models import Estudiante
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def registrar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            estudiante = form.save(commit=False)

            # Generar el código QR
            qr_data = f"Carnet: {estudiante.carnet}, Nombre: {
                estudiante.nombres} {estudiante.apellidos}"
            qr = qrcode.make(qr_data)

            # Guardar el código QR como un archivo en media/qrcodes
            qr_path = f'media/qrcodes/{estudiante.carnet}.png'
            qr.save(qr_path)

            # Enviar el código QR por correo electrónico
            enviar_correo_con_qr(estudiante.correo_electronico, qr_path)

            # Guardar el estudiante en la base de datos
            estudiante.save()

            return HttpResponse("El estudiante ha sido registrado exitosamente.")
    else:
        form = EstudianteForm()

    return render(request, 'formulario_registro_estudiante.html', {'form': form})


def enviar_correo_con_qr(correo_electronico, qr_path):
    # Configurar el correo electrónico
    email = EmailMessage(
        subject='Confirmación de asistencia al simposio',
        body='¡Gracias por registrarte! Adjunto se encuentra tu código QR para ingresar al evento.',
        to=[correo_electronico],
    )

    # Adjuntar el código QR al correo electrónico
    email.attach_file(qr_path)

    # Enviar el correo electrónico
    email.send()


def registrar_expositor(request):
    if request.method == 'POST':
        # Procesar los datos del formulario de expositor
        form = ExpositorForm(request.POST)
        if form.is_valid():
            expositor = form.save()

            # Enviar correo de confirmación al expositor
            enviar_correo_confirmacion_expositor(expositor)

            return HttpResponse("El expositor ha sido registrado exitosamente.")
    else:
        form = ExpositorForm()

    return render(request, 'formulario_registro_expositor.html', {'form': form})


def enviar_correo_con_qr2(estudiante):
    # Configurar el correo electrónico
    email = EmailMessage(
        subject='Confirmación de asistencia al simposio',
        body='¡Gracias por registrarte! Adjunto se encuentra tu código QR para ingresar al evento.',
        to=[estudiante.correo_electronico],
    )

    # Adjuntar el código QR al correo electrónico
    qr_file = estudiante.qr_code
    email.attach(qr_file.name, qr_file.read(), 'image/png')

    # Enviar el correo electrónico
    email.send()


def enviar_correo_confirmacion_expositor(expositor):
    # Configurar el correo electrónico
    email = EmailMessage(
        subject='Confirmación de registro como expositor',
        body='¡Gracias por registrarte como expositor en nuestro simposio!',
        to=[expositor.correo_electronico],
    )

    # Enviar el correo electrónico
    email.send()
