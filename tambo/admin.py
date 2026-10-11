from django.contrib import admin
from .models import Vaca, RegistroCelo
from .models import Vaca, RegistroCelo, PushSubscription

admin.site.register(PushSubscription)

admin.site.register(Vaca)
admin.site.register(RegistroCelo)