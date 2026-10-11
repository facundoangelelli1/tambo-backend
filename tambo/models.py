from django.db import models
from datetime import date

class Vaca(models.Model):
    caravana = models.CharField(max_length=50, unique=True, verbose_name="Número de Caravana")
    activa = models.BooleanField(default=True, verbose_name="Vaca en ordeñe/activa")
    
    def __str__(self):
        return f"Vaca {self.caravana}"

    @property
    def fecha_ultimo_celo(self):
        ultimo = self.historial_celos.order_by('-fecha').first()
        return ultimo.fecha if ultimo else None

class RegistroCelo(models.Model):
    vaca = models.ForeignKey(Vaca, on_delete=models.CASCADE, related_name='historial_celos')
    fecha = models.DateField(default=date.today)
    
    def __str__(self):
        return f"Celo - {self.vaca.caravana} - {self.fecha}"



class PushSubscription(models.Model):
    # La URL única hacia el servidor de Google/Apple
    endpoint = models.URLField(max_length=500, unique=True)
    # Claves de encriptación del navegador
    p256dh = models.CharField(max_length=100)
    auth = models.CharField(max_length=100)
    
    # Opcional: podrías vincularlo a un usuario si usas autenticación
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Suscripción Push: {self.id}"