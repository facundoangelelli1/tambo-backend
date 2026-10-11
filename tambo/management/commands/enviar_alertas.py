from django.core.management.base import BaseCommand
from datetime import date
from django.conf import settings
from pywebpush import webpush, WebPushException
import json
from tambo.models import Vaca, PushSubscription

class Command(BaseCommand):
    help = 'Envía alertas PWA de vacas en celo a los dispositivos suscritos'

    def handle(self, *args, **kwargs):
        hoy = date.today()
        vacas_alerta = []

        # 1. Buscar vacas en la ventana de celo
        for vaca in Vaca.objects.filter(activa=True):
            ultimo_celo = vaca.fecha_ultimo_celo
            if ultimo_celo:
                dias = (hoy - ultimo_celo).days
                if 19 <= dias <= 21:
                    vacas_alerta.append(f"🐄 Caravana {vaca.caravana} (hace {dias} días)")

        if not vacas_alerta:
            self.stdout.write(self.style.SUCCESS('No hay vacas en alerta hoy.'))
            return

        # 2. Armar el mensaje para el celular/PC
        mensaje_texto = "Revisar hoy:\n" + "\n".join(vacas_alerta)
        payload = json.dumps({
            'titulo': '🔥 Alertas de Celo - Tambo',
            'mensaje': mensaje_texto
        })

        # 3. Buscar a quién enviarle la notificación
        suscripciones = PushSubscription.objects.all()
        if not suscripciones.exists():
            self.stdout.write(self.style.WARNING('No hay dispositivos suscritos para recibir alertas.'))
            return

        # 4. Enviar a cada dispositivo
        for sub in suscripciones:
            subscription_info = {
                "endpoint": sub.endpoint,
                "keys": {
                    "p256dh": sub.p256dh,
                    "auth": sub.auth
                }
            }
            
            # --- DIAGNÓSTICO: IMPRIMIR DATOS ---
            print("\n--- DATOS A ENVIAR ---")
            print(f"Endpoint: {sub.endpoint[:30]}...") # Imprime un pedacito de la URL
            print(f"P256dh (Largo: {len(str(sub.p256dh))}): {sub.p256dh}")
            print(f"Auth (Largo: {len(str(sub.auth))}): {sub.auth}")
            print(f"VAPID Email: '{settings.VAPID_ADMIN_EMAIL}'")
            print("----------------------\n")

            try:
                webpush(
                    subscription_info=subscription_info,
                    data=payload,
                    vapid_private_key=settings.VAPID_PRIVATE_KEY,
                    vapid_claims={"sub": settings.VAPID_ADMIN_EMAIL},
                    ttl=86400
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Notificación Push enviada al dispositivo {sub.id}'))
            except WebPushException as e:
                self.stdout.write(self.style.ERROR(f'❌ Error enviando Push: {repr(e)}'))