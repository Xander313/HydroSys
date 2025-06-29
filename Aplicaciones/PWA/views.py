from django.shortcuts import render, redirect

# Create your views here.
def IniciarSesion(request):
    return render(request, 'iniciarSesion/login.html')

