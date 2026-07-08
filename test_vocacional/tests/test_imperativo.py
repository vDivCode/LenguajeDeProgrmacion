from django.test import TestCase
from test_vocacional.paradigmas.controlador_imperativo import TestVocacionalController
from test_vocacional.tests.fixtures import patch_loader

@patch_loader()
class PruebasParadigmaImperativo(TestCase):
    def setUp(self):
        self.controlador = TestVocacionalController()
        self.datos_validos = {
            'int_tecnologia': '5', 'int_salud': '1', 'int_liderazgo': '2',
            'int_arte_diseno': '1', 'int_leyes': '1', 'int_construccion': '1',
            'int_naturaleza': '2', 'int_comunicacion': '1', 'int_economia': '3',
            'int_musica': '1', 'int_ciencias': '4', 'int_persuasion': '1',
            'hab_logica_matematica': '5', 'hab_empatia': '1',
            'hab_espacial': '2', 'hab_destreza_manual': '1', 'hab_verbal': '2',
            'hab_critico': '3',
        }
        self.datos_incompletos = {
            'int_tecnologia': '5',
            # faltan las demás
        }

    def test_validacion_datos(self):
        self.assertTrue(self.controlador.validar_respuestas(self.datos_validos))
        self.assertFalse(self.controlador.validar_respuestas(self.datos_incompletos))
        self.assertGreater(len(self.controlador.errores), 0)

    def test_ejecutar_pipeline_exito(self):
        resultado = self.controlador.ejecutar_pipeline(self.datos_validos)
        self.assertTrue(resultado['exito'])
        self.assertEqual(len(resultado['errores']), 0)
        self.assertGreater(len(resultado['recomendaciones']), 0)
        self.assertEqual(resultado['recomendaciones'][0]['nombre'], 'Desarrollo de Software y Cloud')
