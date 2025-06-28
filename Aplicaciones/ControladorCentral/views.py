from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from Aplicaciones.consumoDinamico.models import ConsumoDinamico
from Aplicaciones.Notificaciones.models import Notificacion
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from Aplicaciones.LimiteUsuario.models import LimiteUsuario
from Aplicaciones.ConsumoEstatico.models import ConsumoEstatico
from Aplicaciones.Notificaciones.models import Notificacion
from Aplicaciones.TipoMensaje.models import TipoMensaje
from datetime import timedelta
from django.utils.timezone import localtime

#python manage.py calcular_consumo_diario
#0 0 * * * /ruta/a/tu/entorno/bin/python /ruta/a/tu/proyecto/manage.py calcular_consumo_diario

from django.db.models import Sum
from datetime import date
from django.utils.timezone import now
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from Aplicaciones.LimiteUsuario.models import LimiteUsuario
from Aplicaciones.Notificaciones.models import Notificacion

from django.utils.timezone import localtime


def construir_mensaje_consumo(nombre, consumo_estatico, consumo_dinamico, consumo_total, umbral, limite_diario):
    fecha_envio = localtime().strftime("%d/%m/%Y %H:%M")
    restante = (umbral - consumo_dinamico) / 1000

    return (
        f"<br>🔵Hola <b>{nombre}</b>, el último corte ha dado los siguientes resultados:<br><br>"

        f"<b>Lectura al inicio de mes:</b> {consumo_estatico / 1000:.2f} m³<br>"
        f"<b>Última lectura:</b> {consumo_total / 1000:.2f} m³<br><br>"
        f"<b>ℹ️ Consumo disponible:</b> {restante:.2f} m³<br><br>"

        f"🔵Aún no supera su <b>límite diario</b> de consumo.<br><br>"
        f"<b>Consumo de hoy:</b> {consumo_dinamico:.2f} L<br>"
        f"<b>Límite diario establecido:</b> {limite_diario:.2f} L<br><br>"


    )




def construir_mensaje_alerta_roja(nombre, consumo_estatico, consumo_dinamico, consumo_total, umbral, limite_diario):
    exceso = consumo_dinamico - umbral
    multa = exceso / 1000
    fecha_envio = localtime().strftime("%d/%m/%Y %H:%M")

    mensaje = (
        f"<br>🔴 Hola <b>{nombre}</b> el último corte ha dado los siguientes resultados:<br><br>"

        f"<b>Lectura al inicio de mes:</b> {consumo_estatico / 1000:.2f} m³<br>"
        f"<b>Última lectura:</b> {consumo_total / 1000:.2f} m³<br><br>"


        f"🔴 Has superado tu <b>Consumo mensual</b> de {umbral / 1000:.2f} m³<br><br>"
        f"<b>Consumo realizado este mes:</b> {consumo_dinamico / 1000:.2f} m³<br>"
        f"<b>Exceso consumido:</b> {exceso / 1000:.2f} m³<br><br>"

        f"A partir de ahora cada m³ consumido tiene un <b>recargo</b> de $1 dólar.<br><br>"

        f"🚨<b>Multa estimada:</b> ${multa:.2f}<br><br>"
    )

    if consumo_dinamico > limite_diario:
        mensaje += (
            f"🟠 También has superado tu <b>límite diario</b> de consumo.<br><br>"
            f"<b>Consumo de hoy:</b> {consumo_dinamico:.2f} L<br>"
            f"<b>Límite diario establecido:</b> {limite_diario:.2f} L<br><br>"
        )
    else:
        mensaje += (
            f"🔵 Aún no supera su <b>límite diario</b> de consumo.<br><br>"
            f"<b>Consumo de hoy:</b> {consumo_dinamico:.2f} L<br>"
            f"<b>Límite diario establecido:</b> {limite_diario:.2f} L<br><br>"
        )

    return mensaje




def construir_mensaje_alerta_naranja(nombre, consumo_estatico, consumo_dinamico, consumo_total, umbral, limite_diario):
    fecha_envio = localtime().strftime("%d/%m/%Y %H:%M")
    restante = (umbral - consumo_dinamico) / 1000
    return (

        f"<br>🟠 Hola <b>{nombre}</b>, el último corte ha dado los siguientes resultados:<br><br>"

        f"<b>Lectura base:</b> {consumo_estatico / 1000:.2f} m³<br>"
        f"<b>Última lectura:</b> {consumo_total / 1000:.2f} m³<br><br>"

        f"<b>ℹ️ Consumo disponible:</b> {restante:.2f} m³<br><br>"

        f"🟠 Has superado tu <b>límite diario</b> de consumo.<br><br>"
        f"<b>Consumo de hoy:</b> {consumo_dinamico:.2f} L<br>"
        f"<b>Límite diario establecido:</b> {limite_diario:.2f} L<br><br>"
    )




def enviar_notificacion(usuario_sensor, mensaje, nombre_tipo):
    try:
        tipo = TipoMensaje.objects.get(tipoAlerta__iexact=nombre_tipo.strip())
        Notificacion.objects.create(
            usuarioSensor=usuario_sensor,
            mensaje=mensaje,
            tipoMensaje=tipo
        )
        print(f"✅ Notificación enviada: {mensaje}")
    except TipoMensaje.DoesNotExist:
        print(f"❌ Tipo de mensaje '{nombre_tipo}' no existe.")




def guardar_consumo(sensor_id, consumo):
    usuario_sensor = UsuarioSensor.objects.filter(sensor__sensorID=sensor_id).first()
    if not usuario_sensor:
        raise ValueError("UsuarioSensor no encontrado")
    
    # Guardar consumo dinámico
    consumo_obj = ConsumoDinamico.objects.create(
        consumoDinamico=consumo,
        usuarioSensor=usuario_sensor
    )
    
    # Obtener configuración de tiempoEnvio para este sensor (en minutos)
    limite = LimiteUsuario.objects.filter(usuarioSensor=usuario_sensor).order_by('-fechaCambio').first()
    if not limite:
        # Configuración por defecto, si no hay límite configurado
        tiempo_envio = 3
        limite_diario = 0
        umbral = 3000  # ejemplo umbral mensual en litros
    else:
        tiempo_envio = limite.tiempoMinutos
        limite_diario = limite.limiteDiario
        umbral = limite.umbralAlerta

    ahora = localtime() 

    inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Obtener última notificación enviada para este sensor (de cualquier tipo)
    ultima_notif = Notificacion.objects.filter(usuarioSensor=usuario_sensor).order_by('-fechaEnvio').first()
    
    # Verificar si ha pasado el tiempo suficiente para enviar nueva notificación
    if ultima_notif is None or (ahora - ultima_notif.fechaEnvio) >= timedelta(minutes=tiempo_envio):
        
        # Calcular consumo diario
        inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        consumo_diario = ConsumoDinamico.objects.filter(
            usuarioSensor=usuario_sensor,
            fechaCorte__gte=inicio_dia
        ).aggregate(total=Sum('consumoDinamico'))['total'] or 0

        # Calcular consumo mensual
        inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        consumo_dinamico_mes = ConsumoDinamico.objects.filter(
            usuarioSensor=usuario_sensor,
            fechaCorte__gte=inicio_mes
        ).aggregate(total=Sum('consumoDinamico'))['total'] or 0

        # Obtener consumo estático
        consumo_estatico = ConsumoEstatico.objects.filter(usuarioSensor=usuario_sensor).order_by('-fechaCorte').first()
        valor_estatico = consumo_estatico.consumoEstatico if consumo_estatico else 0

        # Total del mes
        consumo_total = valor_estatico + consumo_dinamico_mes
        nombre_usuario = usuario_sensor.usuario.nombreUsuario

        # Construcción de mensajes según tipo de alerta
        if consumo_dinamico_mes > umbral:
            mensaje_rojo = construir_mensaje_alerta_roja(nombre_usuario, valor_estatico, consumo_dinamico_mes, consumo_total, umbral, limite_diario)
            enviar_notificacion(usuario_sensor, mensaje_rojo, "Alerta Roja")

        elif consumo_diario > limite_diario:
            mensaje_naranja = construir_mensaje_alerta_naranja(nombre_usuario, valor_estatico, consumo_diario, consumo_total, umbral, limite_diario)
            enviar_notificacion(usuario_sensor, mensaje_naranja, "Alerta Naranja")

        else:
            mensaje_azul = construir_mensaje_consumo(nombre_usuario, valor_estatico, consumo_dinamico_mes, consumo_total, umbral, limite_diario)
            enviar_notificacion(usuario_sensor, mensaje_azul, "Alerta Azul")


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
        print("❌ ValueError:", ve)  # Agregado para depuración
        return JsonResponse({'error': str(ve)}, status=404)

    except Exception as e:
        import traceback
        print("❌ ERROR GENERAL:")
        traceback.print_exc()  # Esto mostrará el error exacto en la consola
        return JsonResponse({'error': 'Error interno', 'detalle': str(e)}, status=500)

