from django.urls import path, include
from . import views
from .views import guardar_suscripcion
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Registramos la ruta 'vacas' que usará tu VacaViewSet
router.register(r'vacas', views.VacaViewSet)



urlpatterns = [
    # Quita el 'api/' de aqui para que no se duplique:
    path('login/', views.login_view, name='login'),
    path('suscripcion-push/', views.guardar_suscripcion, name='guardar_suscripcion'),
    path('alertas-celo/', views.alertas_celo, name='alertas_celo'),
    path('registrar-celo/', views.registrar_celo, name='registrar_celo'),
]








