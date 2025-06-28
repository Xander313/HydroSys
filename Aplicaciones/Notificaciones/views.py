from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from django.http import JsonResponse
from Aplicaciones.Notificaciones.models import Notificacion
from django.core import serializers
from django.utils.timezone import localtime
# Create your views here.

def ver_notificaciones_por_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    sensores = UsuarioSensor.objects.filter(usuario=usuario)
    
    return render(request, 'Notificaciones/panelNotificaciones.html', {
        'usuario': usuario,
        'sensores': sensores,
    })




def obtener_notificaciones_sensor(request, sensor_id):
    notificaciones = Notificacion.objects.filter(usuarioSensor__id=sensor_id).order_by('-fechaEnvio')
    
    data = [
        {
            'mensaje': n.mensaje,
            'fechaEnvio': localtime(n.fechaEnvio).strftime("%Y-%m-%d %H:%M"),  # <- convierte a hora local
            'tipo': n.tipoMensaje.tipoAlerta
        }
        for n in notificaciones
    ]
    
    return JsonResponse({'notificaciones': data})