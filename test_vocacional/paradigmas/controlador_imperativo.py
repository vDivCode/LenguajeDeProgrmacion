"""
=============================================================================
MÓDULO IMPERATIVO/OO - controlador_imperativo.py
=============================================================================
"""
from typing import Dict, Tuple, List, Any
from test_vocacional.datos.constantes import (
    PREGUNTAS_INTERESES, PREGUNTAS_HABILIDADES,
    ID_A_CATEGORIA_INTERES, ID_A_CATEGORIA_HABILIDAD,
    ID_A_TEXTO_PREGUNTA, KNOWLEDGE_BASE
)

class TestVocacionalController:
    def __init__(self):
        self.errores: List[str] = []
        self.advertencias: List[str] = []
        self._intereses_procesados: Dict[str, int] = {}
        self._habilidades_procesadas: Dict[str, int] = {}

    def obtener_estructura_test(self) -> Dict[str, Any]:
        return {
            'preguntas_intereses':  PREGUNTAS_INTERESES,
            'preguntas_habilidades': PREGUNTAS_HABILIDADES,
            'total_preguntas': len(PREGUNTAS_INTERESES) + len(PREGUNTAS_HABILIDADES),
            'total_intereses':   len(PREGUNTAS_INTERESES),
            'total_habilidades': len(PREGUNTAS_HABILIDADES),
        }

    def validar_respuestas(self, datos_post: dict) -> bool:
        self.errores = []
        todas_preguntas = [p['id'] for p in PREGUNTAS_INTERESES] + [p['id'] for p in PREGUNTAS_HABILIDADES]
        for pregunta_id in todas_preguntas:
            valor_raw = datos_post.get(pregunta_id, None)
            texto_legible = ID_A_TEXTO_PREGUNTA.get(pregunta_id, pregunta_id)
            if valor_raw is None or valor_raw == '':
                self.errores.append(f"Falta responder: «{texto_legible}»")
                continue
            try:
                valor = int(valor_raw)
                if not (1 <= valor <= 5):
                    self.errores.append(f"El valor de la pregunta «{texto_legible}» debe estar entre 1 y 5 (recibido: {valor})")
            except (ValueError, TypeError):
                self.errores.append(f"Valor inválido en la pregunta «{texto_legible}»: {valor_raw}")
        return len(self.errores) == 0

    def parsear_respuestas(self, datos_post: dict) -> Tuple[Dict[str, int], Dict[str, int]]:
        intereses = {}
        habilidades = {}
        for pregunta_id, categoria in ID_A_CATEGORIA_INTERES.items():
            try:
                intereses[categoria] = max(1, min(5, int(datos_post.get(pregunta_id, '1'))))
            except (ValueError, TypeError):
                intereses[categoria] = 1
        for pregunta_id, categoria in ID_A_CATEGORIA_HABILIDAD.items():
            try:
                habilidades[categoria] = max(1, min(5, int(datos_post.get(pregunta_id, '1'))))
            except (ValueError, TypeError):
                habilidades[categoria] = 1
        self._intereses_procesados = intereses
        self._habilidades_procesadas = habilidades
        return intereses, habilidades

    def ejecutar_pipeline(self, datos_post: dict) -> Dict[str, Any]:
        from test_vocacional.paradigmas.reglas_logicas import obtener_candidatos, obtener_candidatos_pyDatalog
        from test_vocacional.paradigmas.procesador_funcional import procesar_recomendaciones, calcular_resumen_perfil

        if not self.validar_respuestas(datos_post):
            return {'exito': False, 'errores': self.errores, 'recomendaciones': [], 'perfil': {}}

        intereses, habilidades = self.parsear_respuestas(datos_post)
        try:
            carreras_candidatas = obtener_candidatos_pyDatalog(intereses, habilidades)
        except Exception:
            carreras_candidatas = obtener_candidatos(intereses, habilidades)

        if not carreras_candidatas:
            carreras_candidatas = [row[0] for row in KNOWLEDGE_BASE]
            self.advertencias.append("No se encontraron coincidencias exactas. Te mostramos las mejores opciones disponibles.")

        recomendaciones = procesar_recomendaciones(carreras_candidatas, intereses, habilidades, top_n=5, umbral_min_pct=40.0)
        perfil = calcular_resumen_perfil(intereses, habilidades)

        return {
            'exito': True,
            'errores': [],
            'advertencias': self.advertencias,
            'recomendaciones': recomendaciones,
            'perfil': perfil,
            'total_candidatas_logicas': len(carreras_candidatas),
        }
