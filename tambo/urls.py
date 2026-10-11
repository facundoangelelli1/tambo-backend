from django.urls import path, include
from . import views
from .views import guardar_suscripcion
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Registramos la ruta 'vacas' que usará tu VacaViewSet
router.register(r'vacas', views.VacaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', obtain_auth_token),
    path('api/suscripcion-push/', guardar_suscripcion, name='guardar_suscripcion'),
    path('api/alertas-celo/', views.vacas_en_alerta, name='alertas_celo'),
    path('api/registrar-celo/', views.registrar_celo, name='registrar_celo'),
]








