"""
=============================================================================
MÓDULO FUNCIONAL - procesador_funcional.py
=============================================================================
"""
from functools import reduce
from test_vocacional.datos.constantes import (
    PESO_PRIMARIO, PESO_SECUNDARIO, INTERESES_RELACIONADOS,
    METADATA_CARRERAS, REQUISITOS_CARRERAS
)

def _calcular_bonus_perfil(interes_req: str, intereses: dict) -> float:
    relacionados = INTERESES_RELACIONADOS.get(interes_req, [])
    if not relacionados: return 0.0
    suma = reduce(lambda acc, area: acc + intereses.get(area, 1), relacionados, 0)
    return (suma / (5.0 * len(relacionados))) * 100.0

def calcular_afinidad_v2(carrera: str, intereses: dict, habilidades: dict) -> float:
    interes_req, habilidad_req = REQUISITOS_CARRERAS.get(carrera, ('', ''))
    score_primario = (intereses.get(interes_req, 1) + habilidades.get(habilidad_req, 1)) / 10.0 * 100.0
    score_secundario = _calcular_bonus_perfil(interes_req, intereses)
    return score_primario * PESO_PRIMARIO + score_secundario * PESO_SECUNDARIO

def calcular_afinidad_detallada(carrera: str, intereses: dict, habilidades: dict) -> dict:
    puntaje = calcular_afinidad_v2(carrera, intereses, habilidades)
    interes_req, habilidad_req = REQUISITOS_CARRERAS.get(carrera, ('', ''))
    meta = METADATA_CARRERAS.get(carrera, {'descripcion': '', 'area': '', 'color': '#6B7280'})
    score_int, score_hab = intereses.get(interes_req, 1), habilidades.get(habilidad_req, 1)
    
    return {
        'nombre': carrera, 'puntaje': round(puntaje, 1),
        'interes_clave': interes_req, 'habilidad_clave': habilidad_req,
        'score_interes': score_int, 'score_habilidad': score_hab,
        'pct_primario': round((score_int + score_hab) / 10.0 * 100.0, 1),
        'pct_secundario': round(_calcular_bonus_perfil(interes_req, intereses), 1),
        **meta
    }

def procesar_recomendaciones(candidatas: list, intereses: dict, habilidades: dict, top_n: int = 5, umbral_min_pct: float = 40.0) -> list:
    enriquecidas = list(map(lambda c: calcular_afinidad_detallada(c, intereses, habilidades), candidatas))
    filtradas = list(filter(lambda c: c['puntaje'] >= umbral_min_pct, enriquecidas))
    if not filtradas: filtradas = enriquecidas
    rankeadas = sorted(filtradas, key=lambda c: c['puntaje'], reverse=True)[:top_n]
    return list(map(lambda par: {**par[1], 'rango': par[0] + 1}, enumerate(rankeadas)))

def calcular_resumen_perfil(intereses: dict, habilidades: dict) -> dict:
    total_int = reduce(lambda acc, v: acc + v, intereses.values(), 0)
    total_hab = reduce(lambda acc, v: acc + v, habilidades.values(), 0)
    return {
        'total_intereses': total_int, 'total_habilidades': total_hab,
        'interes_dominante': max(intereses.items(), key=lambda x: x[1], default=('Ninguno', 0))[0],
        'habilidad_dominante': max(habilidades.items(), key=lambda x: x[1], default=('Ninguna', 0))[0],
        'promedio_intereses': round(total_int / max(len(intereses), 1), 2),
        'promedio_habilidades': round(total_hab / max(len(habilidades), 1), 2),
        'top3_intereses': [{'nombre': k, 'score': v} for k, v in sorted(intereses.items(), key=lambda x: x[1], reverse=True)[:3]],
        'top3_habilidades': [{'nombre': k, 'score': v} for k, v in sorted(habilidades.items(), key=lambda x: x[1], reverse=True)[:3]],
        'radar_intereses': [{'label': k, 'value': v} for k, v in sorted(intereses.items(), key=lambda x: x[1], reverse=True)],
        'radar_habilidades': [{'label': k, 'value': v} for k, v in sorted(habilidades.items(), key=lambda x: x[1], reverse=True)],
    }
