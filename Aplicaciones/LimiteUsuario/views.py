from django.shortcuts import render, get_object_or_404, redirect
from Aplicaciones.Usuario.models import Usuario
from .models import LimiteUsuario
from django.utils import timezone


def presentar_limite_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':
        limite_diario = request.POST.get('limiteDiario')
        umbral_alerta = request.POST.get('umbralAlerta')

        if limite_diario and umbral_alerta:
            LimiteUsuario.objects.create(
                usuario=usuario,
                limiteDiario=limite_diario,
                umbralAlerta=umbral_alerta
            )

    limites = LimiteUsuario.objects.filter(usuario=usuario).order_by('-fechaCambio')

    return render(request, 'LimiteUsuario/configuraciones.html', {
        'usuario': usuario,
        'usuarios': [usuario],  # para que el <select> no se rompa
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
