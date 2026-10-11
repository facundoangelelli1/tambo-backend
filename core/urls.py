from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tambo.urls')), # <-- Esto es crucial para que exista /api/...
]