from django.urls import path
from .views import EstudianteListCreate, ExpositorListCreate, PagoListCreate, confirmar_asistencia
from . import views

urlpatterns = [
    path('admin/login/', views.admin_login, name='admin_login'),
    path('estudiantes/', EstudianteListCreate.as_view(), name='estudiante-list'),
    path('expositores/', ExpositorListCreate.as_view(), name='expositor-list'),
    path('pagos/', PagoListCreate.as_view(), name='pago-list'),
    path('confirmar-asistencia/<uuid:qr_code>/',
         confirmar_asistencia, name='confirmar_asistencia'),
]
