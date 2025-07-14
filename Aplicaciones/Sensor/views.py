from django.shortcuts import render, redirect, get_object_or_404
from .models import Sensor
from Aplicaciones.Usuario.models import Usuario
from django.contrib import messages

def agregar_sensor(request):
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        sensorID = request.POST.get('sensorID')
        nombreSensor = request.POST.get('nombreSensor')
        usuario_id = request.POST.get('usuario_id')
        usuario = get_object_or_404(Usuario, id=usuario_id)

        nuevo_sensor = Sensor(sensorID=sensorID, nombreSensor=nombreSensor, usuario=usuario)
        nuevo_sensor.save()

        messages.success(request, 'Sensor agregado correctamente.')
        return redirect('panel_admin')

    return render(request, 'admin/agregar_sensor.html', {'usuarios': usuarios})

def editar_sensor(request, sensorID):
    sensor = get_object_or_404(Sensor, sensorID=sensorID)
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        sensor.nombreSensor = request.POST.get('nombreSensor')
        usuario_id = request.POST.get('usuario_id')
        sensor.usuario = get_object_or_404(Usuario, id=usuario_id)
        sensor.save()
        messages.success(request, 'Sensor actualizado correctamente.')
        return redirect('panel_admin')
    return render(request, 'admin/editar_sensor.html', {'sensor': sensor, 'usuarios': usuarios})

def eliminar_sensor(request, sensorID):
    sensor = get_object_or_404(Sensor, sensorID=sensorID)
    sensor.delete()
    messages.success(request, 'Sensor eliminado correctamente.')
    return redirect('panel_admin')