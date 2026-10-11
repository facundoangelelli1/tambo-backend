from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from .models import Vaca, RegistroCelo
from rest_framework import status
from .models import PushSubscription
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from .serializers import VacaSerializer



from rest_framework.authentication import TokenAuthentication


class VacaViewSet(viewsets.ModelViewSet):
    queryset = Vaca.objects.all()
    serializer_class = VacaSerializer
    
    # 1. Le decimos a Django que busque el Token en las peticiones
    authentication_classes = [TokenAuthentication]
    
    # 2. Le decimos que solo los autenticados pueden modificar (crear/borrar)
    permission_classes = [IsAuthenticatedOrReadOnly]










@api_view(['POST'])
def guardar_suscripcion(request):
    # React (Web Push) envía los datos con una estructura específica
    endpoint = request.data.get('endpoint')
    keys = request.data.get('keys', {})
    p256dh = keys.get('p256dh')
    auth = keys.get('auth')

    if not endpoint or not p256dh or not auth:
        return Response({'error': 'Faltan datos de suscripción'}, status=status.HTTP_400_BAD_REQUEST)

    # update_or_create evita que guardemos duplicados si el usuario recarga la página
    PushSubscription.objects.update_or_create(
        endpoint=endpoint,
        defaults={
            'p256dh': p256dh,
            'auth': auth
        }
    )
    
    return Response({'mensaje': 'Suscripción guardada exitosamente'}, status=status.HTTP_200_OK)




# 1. API para obtener vacas en ventana de celo (19 a 21 días)
@api_view(['GET'])
def vacas_en_alerta(request):
    hoy = date.today()
    vacas_alerta = []
    
    for vaca in Vaca.objects.filter(activa=True):
        ultimo_celo = vaca.fecha_ultimo_celo
        if ultimo_celo:
            dias_transcurridos = (hoy - ultimo_celo).days
            
            # Si pasaron entre 19 y 21 días, la agregamos a la alerta
            if 19 <= dias_transcurridos <= 21:
                vacas_alerta.append({
                    "id": vaca.id,
                    "caravana": vaca.caravana,
                    "ultimo_celo": ultimo_celo.strftime("%Y-%m-%d"),
                    "dias_transcurridos": dias_transcurridos
                })
                
    return Response(vacas_alerta)

# 2. API para que el botón verde de la app registre un celo
@api_view(['POST'])
def registrar_celo(request):
    vaca_id = request.data.get('vaca_id')
    
    # Si la app manda fecha la usamos, si no, usamos la de hoy
    fecha_str = request.data.get('fecha', date.today().strftime("%Y-%m-%d"))
    
    try:
        vaca = Vaca.objects.get(id=vaca_id)
        RegistroCelo.objects.create(vaca=vaca, fecha=fecha_str)
        return Response({"mensaje": f"Celo registrado para vaca {vaca.caravana}", "status": "ok"})
    except Vaca.DoesNotExist:
        return Response({"error": "Vaca no encontrada"}, status=404)