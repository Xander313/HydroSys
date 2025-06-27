from django.shortcuts import render

# Create your views here.
def IniciarSesion(request):
    return render(request, 'iniciarSesion/login.html')