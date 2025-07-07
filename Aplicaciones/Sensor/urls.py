from django.urls import path
from .views import agregar_sensor, editar_sensor, eliminar_sensor

urlpatterns = [
    path('agregar_sensor/', agregar_sensor, name='agregar_sensor'),
    path('editar_sensor/<int:id>/', editar_sensor, name='editar_sensor'),
    path('eliminar_sensor/<int:id>/', eliminar_sensor, name='eliminar_sensor'),



]