from django.urls import path
from . import views

urlpatterns = [
    # Ruta específica primero (resuelve el fetch)
    path('notificaciones/<int:sensor_id>/', views.obtener_notificaciones_sensor, name='obtener_notificaciones_sensor'),

    # Luego las más generales
    path('notificaciones/sensor/<int:id>/', views.ver_notificaciones_por_usuario, name="ver_notificaciones_por_usuario"),


    path('estadisticaPresenracion/', views.ver_notificaciones_por_usuario, name="ver_notificaciones_por_usuario"),

]