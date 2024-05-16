# simposio_app/admin.py

from django.contrib import admin
from .models import Estudiante, Expositor
from django.utils.safestring import mark_safe


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'carnet',
                    'correo_electronico', 'telefono', 'asistencia')
    list_filter = ('asistencia',)
    search_fields = ('nombres', 'apellidos', 'carnet')

    def boleta_de_pago_img(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.boleta_de_pago.url,
            width=obj.boleta_de_pago.width,
            height=obj.boleta_de_pago.height,
        ))

    boleta_de_pago_img.short_description = 'Boleta de Pago'


@admin.register(Expositor)
class ExpositorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'correo_electronico', 'telefono')
    search_fields = ('nombres', 'apellidos')
