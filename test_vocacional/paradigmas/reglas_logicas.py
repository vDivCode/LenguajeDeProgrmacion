"""
=============================================================================
MÓDULO LÓGICO - reglas_logicas.py
=============================================================================
"""
# pyrefly: ignore [missing-import]
from pyDatalog import pyDatalog
from test_vocacional.datos.constantes import UMBRAL_MINIMO, KNOWLEDGE_BASE

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    # Declaraciones estáticas para evitar que el linter del IDE marque "variables indefinidas"
    PD_Carrera = PD_Interes = PD_Habilidad = PD_Score1 = PD_Score2 = Any
    pd_carrera_req = pd_tiene_int = pd_tiene_hab = pd_candidato = Any

pyDatalog.create_terms('PD_Carrera, PD_Interes, PD_Habilidad, PD_Score1, PD_Score2, pd_carrera_req, pd_tiene_int, pd_tiene_hab, pd_candidato')

for _carrera, _interes, _habilidad in KNOWLEDGE_BASE:
    pyDatalog.assert_fact('pd_carrera_req', _carrera, _interes, _habilidad)

pd_candidato(PD_Carrera) <= (
    pd_carrera_req(PD_Carrera, PD_Interes, PD_Habilidad) &
    pd_tiene_int('usuario_activo', PD_Interes, PD_Score1) & (PD_Score1 >= UMBRAL_MINIMO) &
    pd_tiene_hab('usuario_activo', PD_Habilidad, PD_Score2) & (PD_Score2 >= UMBRAL_MINIMO)
)

def obtener_candidatos_pyDatalog(intereses_usuario: dict, habilidades_usuario: dict) -> list:
    todos_intereses   = list({row[1] for row in KNOWLEDGE_BASE})
    todas_habilidades = list({row[2] for row in KNOWLEDGE_BASE})

    for interes in todos_intereses:
        score = intereses_usuario.get(interes, 1)
        pyDatalog.assert_fact('pd_tiene_int', 'usuario_activo', interes, score)

    for habilidad in todas_habilidades:
        score = habilidades_usuario.get(habilidad, 1)
        pyDatalog.assert_fact('pd_tiene_hab', 'usuario_activo', habilidad, score)

    resultado = pd_candidato(PD_Carrera)
    candidatas = [fila[0] for fila in resultado]

    for interes in todos_intereses:
        for score in range(1, 6):
            try: pyDatalog.retract_fact('pd_tiene_int', 'usuario_activo', interes, score)
            except Exception: pass
    for habilidad in todas_habilidades:
        for score in range(1, 6):
            try: pyDatalog.retract_fact('pd_tiene_hab', 'usuario_activo', habilidad, score)
            except Exception: pass

    return candidatas

def obtener_candidatos(intereses_usuario: dict, habilidades_usuario: dict) -> list:
    candidatas = []
    for carrera, interes_req, habilidad_req in KNOWLEDGE_BASE:
        score_interes   = intereses_usuario.get(interes_req, 1)
        score_habilidad = habilidades_usuario.get(habilidad_req, 1)
        if score_interes >= UMBRAL_MINIMO and score_habilidad >= UMBRAL_MINIMO:
            candidatas.append(carrera)
    return candidatas
