from django.shortcuts import render, get_object_or_404
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from Aplicaciones.LimiteUsuario.models import LimiteUsuario

def presentar_limite_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    sensores = UsuarioSensor.objects.filter(usuario=usuario)

    if request.method == 'POST':
        sensor_id = request.POST.get('sensor_id')
        limite_diario = request.POST.get('limiteDiario')
        umbral_alerta = request.POST.get('umbralAlerta')

        if sensor_id and limite_diario and umbral_alerta:
            sensor = get_object_or_404(UsuarioSensor, pk=sensor_id)
            LimiteUsuario.objects.create(
                usuarioSensor=sensor,
                limiteDiario=limite_diario,
                umbralAlerta=umbral_alerta,
                tiempoMinutos=60
            )

    limites = LimiteUsuario.objects.filter(usuarioSensor__usuario=usuario).order_by('-fechaCambio')

    return render(request, 'LimiteUsuario/configuraciones.html', {
        'usuario': usuario,
        'sensores': sensores,
        'limites': limites
    })

def registrar_limite_usuario(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        limite = request.POST.get('limiteDiario')
        umbral = request.POST.get('umbralAlerta')

        LimiteUsuario.objects.create(
            usuario_id=usuario_id,
            limiteDiario=limite,
            umbralAlerta=umbral,
            fechaCambio=timezone.now()
        )

        return redirect('/') 

    usuarios = Usuario.objects.all()
    return render(request, 'LimiteUsuario/configuraciones.html', {'usuarios': usuarios})
