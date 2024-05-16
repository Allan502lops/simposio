# Generated by Django 5.0.3 on 2024-05-15 20:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simposio_app', '0004_remove_estudiante_fecha_nacimiento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='asistencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='fecha_escaneo',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='qr_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='qr_escaneado',
            field=models.BooleanField(default=False),
        ),
    ]