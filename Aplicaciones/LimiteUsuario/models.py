from django.db import models
from Aplicaciones.Usuario.models import Usuario


# Create your models here.

class LimiteUsuario(models.Model):
    limiteUsuarioId = models.AutoField(primary_key=True)
    limiteDiario = models.FloatField()
    umbralAlerta = models.FloatField()
    fechaCambio = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - Límite: {self.limiteDiario} L"
