"""
Configuración de URLs del proyecto Proyecto_TestVocacional.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('test_vocacional.urls')),
]
