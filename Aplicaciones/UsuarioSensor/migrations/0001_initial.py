# Generated by Django 5.2.1 on 2025-06-27 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Sensor', '0001_initial'),
        ('Usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioSensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacionSensor', models.CharField(max_length=100)),
                ('fechaAsignacion', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sensor.sensor')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuario.usuario')),
            ],
            options={
                'unique_together': {('usuario', 'sensor', 'ubicacionSensor')},
            },
        ),
    ]
