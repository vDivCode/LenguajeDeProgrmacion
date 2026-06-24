"""
Configuración de la aplicación test_vocacional.
Define los metadatos de la app para el registro en Django.
"""
from django.apps import AppConfig


class TestVocacionalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_vocacional'
    verbose_name = 'Test Vocacional'
