from django.db import models


class TipoMensaje(models.Model):
    tipoMensajeId = models.AutoField(primary_key=True)
    tipoAlerta = models.CharField(max_length=100)
    mensaje_default = models.TextField()

    def __str__(self):
        return self.tipoAlerta
