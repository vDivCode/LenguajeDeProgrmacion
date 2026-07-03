"""
=============================================================================
MÓDULO LÓGICO - reglas_logicas.py
=============================================================================
"""
# pyrefly: ignore [missing-import]
from pyDatalog import pyDatalog
from test_vocacional.datos.loader import get_knowledge_base, get_config

pyDatalog.create_terms('PD_Carrera, PD_Interes, PD_Habilidad, PD_Score1, PD_Score2, pd_carrera_req, pd_tiene_int, pd_tiene_hab, pd_candidato')

# Cargar reglas desde Supabase (o fallback)
_KNOWLEDGE_BASE = get_knowledge_base()
_UMBRAL_MINIMO  = int(get_config().get('UMBRAL_MINIMO', 3))

for _carrera, _interes, _habilidad in _KNOWLEDGE_BASE:
    pyDatalog.assert_fact('pd_carrera_req', _carrera, _interes, _habilidad)

pd_candidato(PD_Carrera) <= (
    pd_carrera_req(PD_Carrera, PD_Interes, PD_Habilidad) &
    pd_tiene_int('usuario_activo', PD_Interes, PD_Score1) & (PD_Score1 >= _UMBRAL_MINIMO) &
    pd_tiene_hab('usuario_activo', PD_Habilidad, PD_Score2) & (PD_Score2 >= _UMBRAL_MINIMO)
)

def obtener_candidatos_pyDatalog(intereses_usuario: dict, habilidades_usuario: dict) -> list:
    todos_intereses   = list({row[1] for row in _KNOWLEDGE_BASE})
    todas_habilidades = list({row[2] for row in _KNOWLEDGE_BASE})

    for interes in todos_intereses:
        pyDatalog.assert_fact('pd_tiene_int', 'usuario_activo', interes, intereses_usuario.get(interes, 1))

    for habilidad in todas_habilidades:
        pyDatalog.assert_fact('pd_tiene_hab', 'usuario_activo', habilidad, habilidades_usuario.get(habilidad, 1))

    candidatas = [fila[0] for fila in pd_candidato(PD_Carrera)]

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
    umbral = _UMBRAL_MINIMO
    candidatas = []
    for carrera, interes_req, habilidad_req in _KNOWLEDGE_BASE:
        if (intereses_usuario.get(interes_req, 1) >= umbral and
                habilidades_usuario.get(habilidad_req, 1) >= umbral):
            candidatas.append(carrera)
    return candidatas
