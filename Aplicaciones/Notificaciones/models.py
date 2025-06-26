from django.db import models
from Aplicaciones.Usuario.models import Usuario
from Aplicaciones.TipoMensaje.models import TipoMensaje

class Notificacion(models.Model):
    notificacionId = models.AutoField(primary_key=True)
    mensaje = models.TextField()
    fechaEnvio = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipoMensaje = models.ForeignKey(TipoMensaje, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.tipoMensaje.tipoAlerta}"
