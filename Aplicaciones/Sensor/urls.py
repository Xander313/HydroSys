from django.urls import path
from . import views

urlpatterns = [
    path('agregar_sensor/', views.agregar_sensor, name='agregar_sensor'),
        path('sensores/editar_sensor/<int:sensorID>/', views.editar_sensor, name='editar_sensor'),

    path('sensores/eliminar_sensor/<int:sensorID>/', views.eliminar_sensor, name='eliminar_sensor'),    



]