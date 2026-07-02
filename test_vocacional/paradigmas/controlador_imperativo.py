"""
=============================================================================
MÓDULO IMPERATIVO/OO - controlador_imperativo.py
=============================================================================
"""
from typing import Dict, Tuple, List, Any
from test_vocacional.datos.loader import (
    get_preguntas_intereses, get_preguntas_habilidades,
    get_id_a_categoria_interes, get_id_a_categoria_habilidad,
    get_id_a_texto_pregunta, get_knowledge_base,
)

class TestVocacionalController:
    def __init__(self):
        self.errores: List[str] = []
        self.advertencias: List[str] = []
        self._intereses_procesados: Dict[str, int] = {}
        self._habilidades_procesadas: Dict[str, int] = {}

    def obtener_estructura_test(self) -> Dict[str, Any]:
        preguntas_int = get_preguntas_intereses()
        preguntas_hab = get_preguntas_habilidades()
        return {
            'preguntas_intereses':   preguntas_int,
            'preguntas_habilidades': preguntas_hab,
            'total_preguntas':       len(preguntas_int) + len(preguntas_hab),
            'total_intereses':       len(preguntas_int),
            'total_habilidades':     len(preguntas_hab),
        }

    def validar_respuestas(self, datos_post: dict) -> bool:
        self.errores = []
        id_a_texto = get_id_a_texto_pregunta()
        todas = (
            [p['id'] for p in get_preguntas_intereses()] +
            [p['id'] for p in get_preguntas_habilidades()]
        )
        for pregunta_id in todas:
            valor_raw = datos_post.get(pregunta_id, None)
            texto = id_a_texto.get(pregunta_id, pregunta_id)
            if valor_raw is None or valor_raw == '':
                self.errores.append(f"Falta responder: «{texto}»")
                continue
            try:
                valor = int(valor_raw)
                if not (1 <= valor <= 5):
                    self.errores.append(f"El valor de «{texto}» debe estar entre 1 y 5 (recibido: {valor})")
            except (ValueError, TypeError):
                self.errores.append(f"Valor inválido en «{texto}»: {valor_raw}")
        return len(self.errores) == 0

    def parsear_respuestas(self, datos_post: dict) -> Tuple[Dict[str, int], Dict[str, int]]:
        intereses   = {}
        habilidades = {}
        for pregunta_id, categoria in get_id_a_categoria_interes().items():
            try:
                intereses[categoria] = max(1, min(5, int(datos_post.get(pregunta_id, '1'))))
            except (ValueError, TypeError):
                intereses[categoria] = 1
        for pregunta_id, categoria in get_id_a_categoria_habilidad().items():
            try:
                habilidades[categoria] = max(1, min(5, int(datos_post.get(pregunta_id, '1'))))
            except (ValueError, TypeError):
                habilidades[categoria] = 1
        self._intereses_procesados  = intereses
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
            carreras_candidatas = [row[0] for row in get_knowledge_base()]
            self.advertencias.append("No se encontraron coincidencias exactas. Te mostramos las mejores opciones disponibles.")

        recomendaciones = procesar_recomendaciones(carreras_candidatas, intereses, habilidades, top_n=5, umbral_min_pct=40.0)
        perfil          = calcular_resumen_perfil(intereses, habilidades)

        return {
            'exito': True,
            'errores': [],
            'advertencias': self.advertencias,
            'recomendaciones': recomendaciones,
            'perfil': perfil,
            'total_candidatas_logicas': len(carreras_candidatas),
        }
