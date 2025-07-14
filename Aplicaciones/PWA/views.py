from django.shortcuts import render, redirect
from django.contrib.auth import logout
from Aplicaciones.Notificaciones.models import Notificacion


# Create your views here.
def IniciarSesion(request):
    return render(request, 'iniciarSesion/login.html')

def panel_admin(request):
    # ...otros contextos...
    notificaciones = Notificacion.objects.select_related('usuarioSensor', 'tipoMensaje').order_by('-fechaEnvio')
    return render(request, 'admin/paneladmin.html', {
        # ...otros contextos...
        'notificaciones': notificaciones,
        # ...otros contextos...
    })

def cerrar_sesion(request):
    # Lógica para cerrar sesión
    logout(request)  # Asegúrate de importar logout desde django.contrib.auth
    return redirect('login')  # Redirige a donde desees