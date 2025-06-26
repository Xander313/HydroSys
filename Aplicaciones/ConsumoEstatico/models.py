from django.db import models
from Aplicaciones.Usuario.models import Usuario 


class ConsumoEstatico(models.Model):
    consumoEstatico = models.FloatField()
    fechaCorte = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.consumoEstatico} L (Corte: {self.fechaCorte.strftime('%Y-%m-%d')})"
