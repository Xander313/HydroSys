from django.shortcuts import render, redirect
from .models import Sensor
from django.contrib import messages

def agregar_sensor(request):
    if request.method == 'POST':
        sensorID = request.POST.get('sensorID')
        nombreSensor = request.POST.get('nombreSensor')

        # Crear un nuevo sensor
        nuevo_sensor = Sensor(sensorID=sensorID, nombreSensor=nombreSensor)
        nuevo_sensor.save()

        messages.success(request, 'Sensor agregado correctamente.')
        return redirect('panel_admin')  # Cambia esto por la vista a la que deseas redirigir

    return render(request, 'admin/agregar_sensor.html')  # Usa el template correcto