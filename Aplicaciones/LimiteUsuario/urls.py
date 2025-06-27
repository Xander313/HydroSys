from django.urls import path
from . import  views

urlpatterns = [
    path('<id>', views.presentar_limite_usuario, name="presentar_limite_usuario"),
    path('configuraciones/', views.registrar_limite_usuario, name="registrar_limite_usuario"),
]