from django.db import models
from Aplicaciones.Usuario.models import Usuario

# Create your models here.
class ConsumoHistorico(models.Model):
    consumoHistoricoId = models.AutoField(primary_key=True)
    consumoTotal = models.FloatField()
    maxConsumo = models.FloatField()
    minConsumo = models.FloatField()
    fechaPeriodo = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Histórico de {self.usuario} - Total: {self.consumoTotal} L"
