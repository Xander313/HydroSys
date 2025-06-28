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






from django.shortcuts import render, get_object_or_404
from Aplicaciones.ConsumoHistorico.models import ConsumoHistorico
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
import json

def reporte_consumo(request, usuario_id, sensor_id):
    usuario_sensor = get_object_or_404(UsuarioSensor, usuario_id=usuario_id, id=sensor_id)

    historico = ConsumoHistorico.objects.filter(
        usuarioSensor=usuario_sensor
    ).order_by('fechaPeriodo')

    datos = {
        "fechas": [h.fechaPeriodo.strftime('%d/%m') for h in historico],
        "consumo_total": [h.consumoTotal for h in historico],
        "maximo": [h.maxConsumo for h in historico],
        "promedio": [h.minConsumo for h in historico],
    }

    return render(request, "reporte.html", {
        "datos_json": json.dumps(datos),
        "sensor": usuario_sensor.sensor.nombreSensor, 
        "ubicacion": usuario_sensor.ubicacionSensor,   
    })