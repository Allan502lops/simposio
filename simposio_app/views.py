# simposio_app/views.py

from django.utils import timezone
import qrcode
from PIL import Image
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EstudianteForm, ExpositorForm
from .models import Estudiante, Expositor
import uuid
from django.urls import reverse
from django.views.generic import ListView, CreateView
from .models import Estudiante, Expositor, Pago
from django.contrib.auth import authenticate, login
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from io import BytesIO
from django.http import JsonResponse


def estadisticas(request):
    total_estudiantes = Estudiante.objects.count()
    total_expositores = Expositor.objects.count()
    # Otros cálculos de estadísticas

    return render(request, 'estadisticas.html', {
        'total_estudiantes': total_estudiantes,
        'total_expositores': total_expositores,
    })


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            # Redirige al panel de administración
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin/login.html', {'error_message': 'Credenciales inválidas'})
    else:
        return render(request, 'admin/login.html')


@login_required
def estadisticas_estudiantes(request):
    # Código para calcular y mostrar estadísticas de estudiantes
    estudiantes = Estudiante.objects.all()
    total_estudiantes = estudiantes.count()
    # Otros cálculos estadísticos que desees realizar
    return render(request, 'estadisticas_estudiantes.html', {'total_estudiantes': total_estudiantes})


@login_required
def estadisticas_expositores(request):
    # Código para calcular y mostrar estadísticas de expositores
    expositores = Expositor.objects.all()
    total_expositores = expositores.count()
    # Otros cálculos estadísticos que desees realizar
    return render(request, 'estadisticas_expositores.html', {'total_expositores': total_expositores})


class EstudianteListCreate(ListView):
    model = Estudiante
    # El nombre del template que mostrará la lista de estudiantes
    template_name = 'estudiante_list.html'
    # El nombre de la variable de contexto que contendrá la lista de estudiantes
    context_object_name = 'estudiantes'


class ExpositorListCreate(ListView):
    model = Expositor
    # El nombre del template que mostrará la lista de expositores
    template_name = 'expositor_list.html'
    # El nombre de la variable de contexto que contendrá la lista de expositores
    context_object_name = 'expositores'


class PagoListCreate(ListView):
    model = Pago
    # El nombre del template que mostrará la lista de pagos
    template_name = 'pago_list.html'
    # El nombre de la variable de contexto que contendrá la lista de pagos
    context_object_name = 'pagos'


def index(request):
    return render(request, 'formulario_registro_estudiante.html')


def formulario_registro_estudiante(request):
    # Lógica para procesar datos del formulario, si es necesario
    return render(request, 'formulario_registro_estudiante.html')


def registrar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            estudiante = form.save(commit=False)

            # Subir y comprimir la imagen de la boleta de pago
            if 'imagen_boleta_pago' in request.FILES:
                imagen_boleta_pago = request.FILES['imagen_boleta_pago']
                imagen_boleta_comprimida = comprimir_imagen(imagen_boleta_pago)
                buffer = BytesIO()
                imagen_boleta_comprimida.save(
                    buffer, format="JPEG", quality=50)
                estudiante.imagen_boleta_pago = buffer.getvalue()

            # Generar el código QR único
            qr_code = uuid.uuid4()
            estudiante.qr_code = qr_code

            # Generar el código QR
            qr_data = f"Carnet: {estudiante.carnet}, Nombre: {estudiante.nombres}, qr_code: {estudiante.qr_code}"
            qr = qrcode.make(qr_data)

            # Guardar el código QR como un archivo binario
            qr_buffer = BytesIO()
            qr.save(qr_buffer, format="PNG")
            estudiante.qr_code_image = qr_buffer.getvalue()

            # Guardar el estudiante en la base de datos
            estudiante.save()

            # Enviar el código QR por correo electrónico
            enviar_correo_con_qr(
                estudiante.correo_electronico, estudiante.qr_code_image, estudiante)

            return HttpResponse("El estudiante ha sido registrado exitosamente.")
    else:
        form = EstudianteForm()
    return render(request, 'formulario_registro_estudiante.html', {'form': form})


def enviar_correo_con_qr(correo_electronico, qr_code_image, estudiante):
    # Construir el mensaje del correo electrónico
    subject = '¡Confirmación de registro exitosa para el Simposio!'
    body = f'¡Hola {estudiante.nombres} {estudiante.apellidos}!\n\n' \
        f'¡Gracias por registrarte para el simposio! Estamos emocionados de tenerte con nosotros.\n\n' \
        f'Adjunto encontrarás tu código QR personalizado para ingresar al evento. Por favor, asegúrate de llevarlo y no escaneralo ya que solo se puede escanear una vez ' \
        f'contigo el día del simposio.\n\n' \
        f'Detalles de tu registro:\n' \
        f'- Nombre: {estudiante.nombres}\n' \
        f'- Apellidos: {estudiante.apellidos}\n' \
        f'- Carnet: {estudiante.carnet}\n' \
        f'- Código QR: {estudiante.qr_code}\n\n' \
        f'¡Esperamos verte en el simposio y compartir esta experiencia contigo!\n\n' \
        f'¡Gracias de nuevo y hasta pronto!\n\n' \
        f'Atentamente,\n' \
        f'El equipo organizador del Simposio'

    # Configurar el correo electrónico
    email = EmailMessage(
        subject=subject,
        body=body,
        to=[correo_electronico],
    )

    # Adjuntar el código QR al correo electrónico
    email.attach('qr_code.png', qr_code_image, 'image/png')

    # Enviar el correo electrónico
    email.send()


def comprimir_imagen(imagen):
    # Abre la imagen utilizando PIL
    img = Image.open(imagen)
    buffer = BytesIO()

    # Comprime la imagen reduciendo su calidad a un 50%
    img_comprimida = img.convert('RGB')
    img_comprimida.save(buffer, format="JPEG", quality=50)

    return Image.open(BytesIO(buffer.getvalue()))


def confirmar_asistencia(request, qr_code):
    estudiante = get_object_or_404(Estudiante, qr_code=qr_code)
    if not estudiante.qr_escaneado:
        # Actualizar el estado del QR
        estudiante.qr_escaneado = True
        estudiante.fecha_escaneo = timezone.now()
        estudiante.save()

        # Actualizar el estado de asistencia
        estudiante.asistencia = True
        estudiante.save()

        # Redireccionar a la página de confirmación de asistencia
        return render(request, 'confirmacion_asistencia.html', {'estudiante': estudiante})
    else:
        # Si el QR ya ha sido escaneado, redirigir a alguna página de error
        return HttpResponseRedirect(reverse('pagina_de_error'))


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


def enviar_correo_confirmacion_expositor(expositor):
    # Construir el mensaje del correo electrónico
    subject = '¡Confirmación de registro como expositor!'
    body = f'¡Hola {expositor.nombres}!\n\n' \
           f'¡Gracias por registrarte como expositor en nuestro simposio! Estamos emocionados de tenerte con nosotros.\n\n' \
           f'¡Esperamos que tengas una experiencia increíble compartiendo tu conocimiento con nuestros asistentes!\n\n' \
           f'Atentamente,\n' \
           f'El equipo organizador del Simposio'
    
    # Configurar el correo electrónico
    email = EmailMessage(
        subject=subject,
        body=body,
        to=[expositor.correo_electronico],
    )

    # Enviar el correo electrónico
    email.send()