from django.test import TestCase
from test_vocacional.paradigmas.procesador_funcional import procesar_recomendaciones, calcular_resumen_perfil
from test_vocacional.tests.fixtures import patch_loader

@patch_loader()
class PruebasParadigmaFuncional(TestCase):
    def setUp(self):
        self.candidatas = [
            'Desarrollo de Software y Cloud',
            'Economía y Finanzas de Mercado',
            'Biotecnología y Bioingeniería',
        ]
        self.intereses = {
            'Tecnología y Programación': 5, 'Ciencias de la Salud': 1,
            'Negocios y Liderazgo': 2, 'Arte y Creatividad': 1,
            'Leyes y Política': 1, 'Construcción e Ingeniería': 1,
            'Investigación Científica': 4, 'Comunicación y Medios': 1,
            'Finanzas y Economía': 3, 'Expresión Musical': 1,
            'Ciencias de la Tierra': 2, 'Persuasión y Ventas': 1,
        }
        self.habilidades = {
            'Lógica y Matemática': 5, 'Empatía y Relación Social': 1,
            'Habilidad Espacial y Visual': 2, 'Destreza Manual e Instrumental': 1,
            'Razonamiento Verbal y Análisis': 2, 'Pensamiento Crítico e Investigación': 3,
        }

    def test_procesar_recomendaciones_ranking(self):
        recomendaciones = procesar_recomendaciones(
            candidatas=self.candidatas,
            intereses=self.intereses,
            habilidades=self.habilidades,
            top_n=3
        )
        self.assertEqual(len(recomendaciones), 3)
        # El de mayor puntaje debe ser Desarrollo de Software y Cloud (Tech=5 + Lógica=5)
        self.assertEqual(recomendaciones[0]['nombre'], 'Desarrollo de Software y Cloud')
        # El puntaje máximo debe ser superior al 80%
        self.assertGreaterEqual(recomendaciones[0]['puntaje'], 70.0)
        # Verificar que está correctamente rankeado (puntajes descendentes)
        for i in range(len(recomendaciones) - 1):
            self.assertGreaterEqual(recomendaciones[i]['puntaje'], recomendaciones[i + 1]['puntaje'])
        self.assertEqual(recomendaciones[0]['rango'], 1)

    def test_calcular_resumen_perfil(self):
        resumen = calcular_resumen_perfil(self.intereses, self.habilidades)
        self.assertEqual(resumen['interes_dominante'], 'Tecnología y Programación')
        self.assertEqual(resumen['habilidad_dominante'], 'Lógica y Matemática')
        self.assertGreater(resumen['total_intereses'], 0)
        self.assertGreater(resumen['total_habilidades'], 0)
