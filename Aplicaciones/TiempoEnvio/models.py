from django.db import models
from Aplicaciones.Usuario.models import Usuario

# Create your models here.

class TiempoEnvio(models.Model):
    tiempoEnvioId = models.AutoField(primary_key=True)
    tiempoSegundos = models.IntegerField()
    fechaCambio = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.tiempoSegundos} seg"
