from django.urls import path
from . import views

urlpatterns = [
    ################ ESTA RUTA ES PARA EL MENU CENTRAL##############
    path('sesionIniciada/', views.menuCentral, name='menuCentral'), 

    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

]