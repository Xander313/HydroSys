from django.shortcuts import render

# Create your views here.
def perfil_usuario(request):
    return render(request, 'Usuario/perfil.html')


    
def menuCentral(request):
    return render(request, 'Usuario/menuCentral.html')