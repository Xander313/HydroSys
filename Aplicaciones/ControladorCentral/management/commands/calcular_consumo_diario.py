from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date, datetime
from Aplicaciones.UsuarioSensor.models import UsuarioSensor
from Aplicaciones.consumoDinamico.models import ConsumoDinamico
from Aplicaciones.ConsumoHistorico.models import ConsumoHistorico
from Aplicaciones.Usuario.models import Usuario

class Command(BaseCommand):
    help = "Calcula el consumo diario por usuario y lo guarda en ConsumoHistorico"

    def handle(self, *args, **kwargs):
        hoy = timezone.localdate()
        ayer = hoy - timedelta(days=1)

        inicio = timezone.make_aware(datetime.combine(ayer, datetime.min.time()))
        fin = timezone.make_aware(datetime.combine(ayer, datetime.max.time()))

        for usuario in Usuario.objects.all():
            sensores = UsuarioSensor.objects.filter(usuario=usuario)

            consumos = ConsumoDinamico.objects.filter(
                usuarioSensor__in=sensores,
                fechaCorte__range=(inicio, fin)
            )

            if consumos.exists():
                total = sum(c.consumoDinamico for c in consumos)
                maximo = max(c.consumoDinamico for c in consumos)
                minimo = min(c.consumoDinamico for c in consumos)

                ConsumoHistorico.objects.create(
                    consumoTotal=total,
                    maxConsumo=maximo,
                    minConsumo=minimo,
                    fechaPeriodo=ayer,
                    usuario=usuario
                )
                self.stdout.write(f"✅ Histórico registrado para {usuario} ({ayer})")
            else:
                self.stdout.write(f"⚠️ No hay datos para {usuario} en {ayer}")
