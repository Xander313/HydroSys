from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Usuario
import uuid
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import random
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correoUsuario')
        password = request.POST.get('passwordUsuario')
        
        # Verificación especial para admin
        if correo == 'admin' and password == '1234':
            request.session['es_admin'] = True
            return redirect('menuCentral')  # Redirige al menú central para admin
        
        try:
            usuario = Usuario.objects.get(correoUsuario=correo)
            if check_password(password, usuario.passwordUsuario):
                request.session['usuario_id'] = usuario.id
                return redirect('menuCentral')  # Redirige al menú central para usuarios
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            
    return render(request, 'iniciarSesion/login.html')


def registro(request):
    if request.method == 'POST':
        correo = request.POST.get('correoUsuario')
        password = request.POST.get('passwordUsuario')
        
        # Generar un código de verificación
        verification_code = random.randint(100000, 999999)
        
        # Enviar el correo de verificación
        send_mail(
            'Código de Verificación',
            f'Tu código de verificación es: {verification_code}',
            'tu_correo@example.com',  # Cambia esto por tu correo
            [correo],
            fail_silently=False,
        )
        
        # Guardar el código en la sesión para verificarlo después
        request.session['verification_code'] = verification_code
        request.session['correo'] = correo
        request.session['password'] = password
        
        messages.success(request, 'Se ha enviado un código de verificación a tu correo electrónico.')
        return redirect('verify_email')  # Redirigir a la página de verificación
    return render(request, 'iniciarSesion/login.html', {'show_register': True})


# no tocar
def perfil_usuario(request):
    return render(request, 'Usuario/perfil.html')


    
def menuCentral(request):
    return render(request, 'Usuario/menuCentral.html')