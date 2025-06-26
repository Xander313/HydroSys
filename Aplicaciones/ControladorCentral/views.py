from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from Aplicaciones.consumoDinamico.models import ConsumoDinamico

def guardar_consumo(sensor_id, consumo):
    usuario_sensor = UsuarioSensor.objects.filter(sensor__sensor_id=sensor_id).first()
    if not usuario_sensor:
        raise ValueError("UsuarioSensor no encontrado")
    consumo_obj = ConsumoDinamico.objects.create(
        consumoDinamico=consumo,
        usuarioSensor=usuario_sensor
    )
    
    return consumo_obj

@csrf_exempt
def recibir_datos_esp32(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Solo POST permitido'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
        sensor_id = data.get('sensor_id')
        consumo = data.get('consumoLitro')
        if not sensor_id or consumo is None:
            return JsonResponse({'error': 'Faltan datos'}, status=400)
        guardar_consumo(sensor_id, consumo)
        return JsonResponse({'mensaje': 'Lectura guardada'}, status=200)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Error interno', 'detalle': str(e)}, status=500)
