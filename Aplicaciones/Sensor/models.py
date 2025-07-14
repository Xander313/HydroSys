from django.db import models
from Aplicaciones.Usuario.models import Usuario

# Create your models here.
class Sensor(models.Model):
    sensorID = models.IntegerField(primary_key=True)
    nombreSensor = models.CharField(max_length=100)
    fechaInscripcion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación foránea

    

    def __str__(self):
        return self.nombreSensor