from django.urls import path
from .views import agregar_sensor

urlpatterns = [
    path('agregar_sensor/', agregar_sensor, name='agregar_sensor'),

]