from django.urls import path
from . import views 

urlpatterns = [
    path('notificaciones/<int:sensor_id>/', views.obtener_notificaciones_sensor, name='obtener_notificaciones_sensor'),

    path('notificaciones/sensor/<int:id>/', views.ver_notificaciones_por_usuario, name="ver_notificaciones_por_usuario"),


    path('notificaciones/', views.lista_notificaciones, name='lista_notificaciones'),
    path('notificaciones/editar/<int:id>/', views.editar_notificacion, name='editar_notificacion'),
    path('notificaciones/eliminar/<int:id>/', views.eliminar_notificacion, name='eliminar_notificacion'),


    path('estadistica/<id>', views.estadisticaPresenracion, name="estadisticaPresenracion"),


    path("reporte/consumo/<int:sensor_id>/", views.reporte_consumo_json, name="reporte_consumo_json"),

    path("reporte/consumo/pie/<int:sensor_id>/", views.reporte_consumo_pie, name="reporte_consumo_pie"),




]