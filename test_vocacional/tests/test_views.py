from django.test import TestCase, Client, override_settings
from django.urls import reverse
import json
from test_vocacional.tests.fixtures import patch_loader

@patch_loader()
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PruebasVistasDjango(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.datos_post = {
            'int_tecnologia': '5', 'int_salud': '1', 'int_liderazgo': '2',
            'int_arte_diseno': '1', 'int_leyes': '1', 'int_construccion': '1',
            'int_naturaleza': '2', 'int_comunicacion': '1', 'int_economia': '3',
            'int_musica': '1', 'int_ciencias': '4', 'int_persuasion': '1',
            'hab_logica_matematica': '5', 'hab_empatia': '1',
            'hab_espacial': '2', 'hab_destreza_manual': '1', 'hab_verbal': '2',
            'hab_critico': '3',
        }

    def test_vista_home(self):
        respuesta = self.cliente.get(reverse('test_vocacional:home'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Brújula Vocacional")

    def test_vista_test_get(self):
        respuesta = self.cliente.get(reverse('test_vocacional:test'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "¿Qué tanto te interesa el desarrollo de software")

    def test_vista_test_post_valido(self):
        respuesta = self.cliente.post(reverse('test_vocacional:test'), data=self.datos_post)
        # Debe redirigir a la página de resultados
        self.assertRedirects(respuesta, reverse('test_vocacional:resultados'))

        # Verificar que la página de resultados carga correctamente
        respuesta_resultados = self.cliente.get(reverse('test_vocacional:resultados'))
        self.assertEqual(respuesta_resultados.status_code, 200)
        self.assertContains(respuesta_resultados, "Desarrollo de Software y Cloud")
