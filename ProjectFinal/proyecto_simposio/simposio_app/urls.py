#simposio_app/urls.py

from django.urls import path
from .views import EstudianteListCreate, ExpositorListCreate, PagoListCreate

urlpatterns = [
    path('estudiantes/', EstudianteListCreate.as_view(), name='estudiante-list-create'),
    path('expositores/', ExpositorListCreate.as_view(), name='expositor-list-create'),
    path('pagos/', PagoListCreate.as_view(), name='pago-list-create'),
]
