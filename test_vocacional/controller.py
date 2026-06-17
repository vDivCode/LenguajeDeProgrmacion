"""
=============================================================================
MÓDULO IMPERATIVO/OO - controller.py
=============================================================================
Paradigma: IMPERATIVO / ORIENTADO A OBJETOS
Patrón:    Controlador (Coordinador del flujo)

Este módulo contiene la clase TestVocacionalController, que es el centro
orquestador del sistema. Implementa el flujo imperativo:
  1. Recibe respuestas del usuario desde la interfaz web.
  2. Valida y estructura los datos de entrada.
  3. Coordina la llamada al módulo lógico (logic_rules).
  4. Coordina la llamada al módulo funcional (processor).
  5. Devuelve los resultados listos para la vista.

También define la estructura de las preguntas del test.
=============================================================================
"""


# ---------------------------------------------------------------------------
# 1. Definición de las preguntas del test
#    Cada pregunta tiene un ID, un texto y la categoría que mide.
# ---------------------------------------------------------------------------
PREGUNTAS_INTERESES = [
    {
        'id': 'int_tecnologia',
        'categoria': 'Tecnología y Programación',
        'texto': '¿Qué tanto te interesa el desarrollo de software, la programación y el diseño de sistemas informáticos o en la nube?',
    },
    {
        'id': 'int_salud',
        'categoria': 'Ciencias de la Salud',
        'texto': '¿Te atrae el estudio de la medicina, la anatomía, el diagnóstico clínico y el cuidado físico o mental de los pacientes?',
    },
    {
        'id': 'int_liderazgo',
        'categoria': 'Negocios y Liderazgo',
        'texto': '¿Cuánto te interesa dirigir equipos de trabajo, planificar estrategias corporativas y coordinar el crecimiento de organizaciones?',
    },
    {
        'id': 'int_arte_diseno',
        'categoria': 'Arte y Creatividad',
        'texto': '¿Qué tanto disfrutas expresarte mediante las artes visuales, la animación digital, el diseño de interfaces o la actuación?',
    },
    {
        'id': 'int_leyes',
        'categoria': 'Leyes y Política',
        'texto': '¿Te interesa analizar el marco legal, las políticas públicas, la defensa de los derechos ciudadanos y la justicia social?',
    },
    {
        'id': 'int_construccion',
        'categoria': 'Construcción e Ingeniería',
        'texto': '¿Te atrae el diseño estructural de edificios, la robótica industrial, el funcionamiento de máquinas o la planificación de obras?',
    },
    {
        'id': 'int_naturaleza',
        'categoria': 'Ciencias de la Tierra',
        'texto': '¿Cuánto te apasiona la ecología, el impacto de las energías renovables y la conservación del medio ambiente y los recursos naturales?',
    },
    {
        'id': 'int_comunicacion',
        'categoria': 'Comunicación y Medios',
        'texto': '¿Qué tanto te interesa la redacción periodística, la producción audiovisual y la comunicación de información en plataformas digitales?',
    },
    {
        'id': 'int_economia',
        'categoria': 'Finanzas y Economía',
        'texto': '¿Te atrae analizar los mercados financieros, la asignación de recursos económicos y las estrategias de inversión o comercio?',
    },
    {
        'id': 'int_musica',
        'categoria': 'Expresión Musical',
        'texto': '¿Cuánto te interesa la teoría musical, la composición, la interpretación de instrumentos o la producción de audio?',
    },
    {
        'id': 'int_ciencias',
        'categoria': 'Investigación Científica',
        'texto': '¿Te apasiona la experimentación en laboratorios, el estudio de la bioquímica, la genética o el desarrollo de nuevos fármacos?',
    },
    {
        'id': 'int_persuasion',
        'categoria': 'Persuasión y Ventas',
        'texto': '¿Qué tanto disfrutas diseñar campañas publicitarias, negociar acuerdos comerciales o convencer a un público de adoptar una idea?',
    },
]

PREGUNTAS_HABILIDADES = [
    {
        'id': 'hab_logica_matematica',
        'categoria': 'Lógica y Matemática',
        'texto': '¿Qué nivel de facilidad tienes para resolver problemas matemáticos, aplicar el pensamiento abstracto y analizar datos estructurados?',
    },
    {
        'id': 'hab_empatia',
        'categoria': 'Empatía y Relación Social',
        'texto': '¿Qué tan bien logras comprender las emociones de los demás, comunicarte con sensibilidad y resolver conflictos interpersonales?',
    },
    {
        'id': 'hab_espacial',
        'categoria': 'Habilidad Espacial y Visual',
        'texto': '¿Qué tan desarrollado tienes el sentido de orientación, la visualización de volúmenes en tres dimensiones y el dibujo técnico?',
    },
    {
        'id': 'hab_destreza_manual',
        'categoria': 'Destreza Manual e Instrumental',
        'texto': '¿Qué facilidad posees para manipular herramientas con precisión, tocar instrumentos musicales o realizar trabajos que exigen coordinación motora fina?',
    },
    {
        'id': 'hab_verbal',
        'categoria': 'Razonamiento Verbal y Análisis',
        'texto': '¿Qué tan bueno/a eres para redactar informes detallados, argumentar ideas complejas por escrito y debatir con claridad?',
    },
    {
        'id': 'hab_critico',
        'categoria': 'Pensamiento Crítico e Investigación',
        'texto': '¿Qué tan desarrollado tienes el hábito de cuestionar hechos, investigar hipótesis científicas y evaluar objetivamente la validez de la información?',
    },
]

# Mapa de ID de pregunta a categoría (para parseo rápido)
ID_A_CATEGORIA_INTERES   = {p['id']: p['categoria'] for p in PREGUNTAS_INTERESES}
ID_A_CATEGORIA_HABILIDAD = {p['id']: p['categoria'] for p in PREGUNTAS_HABILIDADES}

# Mapa de ID de pregunta a texto legible (para mensajes de error amigables)
ID_A_TEXTO_PREGUNTA = {
    p['id']: p['texto'][:80] + '…'
    for p in PREGUNTAS_INTERESES + PREGUNTAS_HABILIDADES
}


# ---------------------------------------------------------------------------
# 2. Clase controladora principal (OO + Imperativo)
# ---------------------------------------------------------------------------
class TestVocacionalController:
    """
    Controlador principal del sistema de test vocacional.

    Coordina el flujo de datos entre la interfaz web, el módulo lógico
    y el módulo funcional. Implementa el paradigma imperativo mediante
    control de flujo explícito, validación de estado y manejo de eventos.
    """

    def __init__(self):
        self.errores = []
        self.advertencias = []
        self._intereses_procesados = {}
        self._habilidades_procesadas = {}

    def obtener_estructura_test(self) -> dict:
        """
        OO: Devuelve la estructura completa del test para renderizar la UI.
        """
        return {
            'preguntas_intereses':  PREGUNTAS_INTERESES,
            'preguntas_habilidades': PREGUNTAS_HABILIDADES,
            'total_preguntas': len(PREGUNTAS_INTERESES) + len(PREGUNTAS_HABILIDADES),
            'total_intereses':   len(PREGUNTAS_INTERESES),
            'total_habilidades': len(PREGUNTAS_HABILIDADES),
        }

    def validar_respuestas(self, datos_post: dict) -> bool:
        """
        Imperativo: Valida que todas las respuestas estén presentes y en rango.
        Los mensajes de error usan el texto legible de la pregunta, no el ID técnico.

        Retorna True si todas las respuestas son válidas.
        """
        self.errores = []
        todas_preguntas = (
            [p['id'] for p in PREGUNTAS_INTERESES] +
            [p['id'] for p in PREGUNTAS_HABILIDADES]
        )

        # Control de flujo imperativo: iterar y validar cada pregunta
        for pregunta_id in todas_preguntas:
            valor_raw = datos_post.get(pregunta_id, None)
            texto_legible = ID_A_TEXTO_PREGUNTA.get(pregunta_id, pregunta_id)

            if valor_raw is None or valor_raw == '':
                self.errores.append(
                    f"Falta responder: «{texto_legible}»"
                )
                continue
            try:
                valor = int(valor_raw)
                if not (1 <= valor <= 5):
                    self.errores.append(
                        f"El valor de la pregunta «{texto_legible}» debe estar entre 1 y 5 (recibido: {valor})"
                    )
            except (ValueError, TypeError):
                self.errores.append(
                    f"Valor inválido en la pregunta «{texto_legible}»: {valor_raw}"
                )

        return len(self.errores) == 0

    def parsear_respuestas(self, datos_post: dict) -> tuple[dict, dict]:
        """
        Imperativo: Extrae y estructura los scores de interés y habilidad
        desde los datos POST del formulario web.

        Retorna:
            tuple: (dict_intereses, dict_habilidades)
                   Ej: ({'Tecnología': 5, 'Salud': 2, ...}, {'Empatía': 3, ...})
        """
        intereses = {}
        habilidades = {}

        # Parsear intereses
        for pregunta_id, categoria in ID_A_CATEGORIA_INTERES.items():
            valor_raw = datos_post.get(pregunta_id, '1')
            try:
                valor = int(valor_raw)
                valor = max(1, min(5, valor))  # Clamping al rango [1, 5]
            except (ValueError, TypeError):
                valor = 1
            intereses[categoria] = valor

        # Parsear habilidades
        for pregunta_id, categoria in ID_A_CATEGORIA_HABILIDAD.items():
            valor_raw = datos_post.get(pregunta_id, '1')
            try:
                valor = int(valor_raw)
                valor = max(1, min(5, valor))  # Clamping al rango [1, 5]
            except (ValueError, TypeError):
                valor = 1
            habilidades[categoria] = valor

        self._intereses_procesados = intereses
        self._habilidades_procesadas = habilidades
        return intereses, habilidades

    def ejecutar_pipeline(self, datos_post: dict) -> dict:
        """
        Método principal del controlador. Orquesta el pipeline completo:

        Flujo imperativo:
          1. Validar respuestas
          2. Parsear respuestas
          3. Llamar módulo lógico → obtener candidatas (pyDatalog con fallback)
          4. Llamar módulo funcional → obtener ranking
          5. Generar resumen de perfil
          6. Retornar resultados estructurados

        Retorna:
            dict con 'exito', 'errores', 'recomendaciones', 'perfil'
        """
        # Importaciones locales para separación modular clara
        from test_vocacional.logic_rules import (
            obtener_candidatos,
            obtener_candidatos_pyDatalog,
            KNOWLEDGE_BASE
        )
        from test_vocacional.processor import procesar_recomendaciones, calcular_resumen_perfil

        # Paso 1: Validar
        if not self.validar_respuestas(datos_post):
            return {
                'exito': False,
                'errores': self.errores,
                'recomendaciones': [],
                'perfil': {},
            }

        # Paso 2: Parsear
        intereses, habilidades = self.parsear_respuestas(datos_post)

        # Paso 3: PARADIGMA LÓGICO — Inferir candidatas
        # Intentamos primero con pyDatalog puro, y si falla usamos la versión robusta
        try:
            carreras_candidatas = obtener_candidatos_pyDatalog(intereses, habilidades)
        except Exception:
            carreras_candidatas = obtener_candidatos(intereses, habilidades)

        # Si no hay candidatas con el umbral lógico, relajamos para dar respuesta
        if not carreras_candidatas:
            carreras_candidatas = [row[0] for row in KNOWLEDGE_BASE]
            self.advertencias.append(
                "No se encontraron coincidencias exactas. Te mostramos las mejores opciones disponibles."
            )

        # Paso 4: PARADIGMA FUNCIONAL — Rankear y enriquecer candidatas
        recomendaciones = procesar_recomendaciones(
            candidatas=carreras_candidatas,
            intereses=intereses,
            habilidades=habilidades,
            top_n=5,
            umbral_min_pct=40.0
        )

        # Paso 5: Resumen de perfil extendido
        perfil = calcular_resumen_perfil(intereses, habilidades)

        # Paso 6: Retornar resultado estructurado
        return {
            'exito': True,
            'errores': [],
            'advertencias': self.advertencias,
            'recomendaciones': recomendaciones,
            'perfil': perfil,
            'total_candidatas_logicas': len(carreras_candidatas),
        }
