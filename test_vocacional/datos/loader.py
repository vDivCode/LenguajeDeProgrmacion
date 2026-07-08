"""
=============================================================================
MÓDULO LOADER - loader.py
=============================================================================
Carga todos los datos estáticos desde Supabase con caché en memoria.
Los datos se cargan UNA SOLA VEZ al arrancar el servidor.
Si Supabase no está disponible, usa constantes.py como fallback.
=============================================================================
"""

import logging
from functools import lru_cache
from typing import Optional

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# CACHÉ: carga los datos de Supabase una sola vez
# ─────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _cargar_datos_supabase() -> Optional[dict]:
    """
    Hace un único request a Supabase al arrancar y guarda todo en memoria.
    Retorna None si falla, para activar el fallback.
    """
    try:
        from test_vocacional.services.supabase_client import get_client
        client = get_client()
        if client is None:
            return None

        preguntas_raw       = client.table('preguntas').select('*').order('ordem').execute().data
        carreras_raw        = client.table('carreras').select('*').eq('activa', True).execute().data
        reglas_raw          = client.table('reglas_conocimiento').select('*').execute().data
        config_raw          = client.table('config_algoritmo').select('*').execute().data
        relacionados_raw    = client.table('intereses_relacionados').select('*').execute().data

        logger.info("Datos cargados desde Supabase: %d preguntas, %d carreras, %d reglas",
                    len(preguntas_raw), len(carreras_raw), len(reglas_raw))

        return {
            'preguntas':     preguntas_raw,
            'carreras':      carreras_raw,
            'reglas':        reglas_raw,
            'config':        config_raw,
            'relacionados':  relacionados_raw,
        }

    except Exception as exc:
        logger.warning("No se pudo cargar datos de Supabase (%s). Usando fallback local.", exc)
        return None


def _fallback():
    """Fallback si falla Supabase. Devuelve datos vacíos para evitar error 500."""
    return {
        'preguntas':    [],
        'carreras':     [],
        'reglas':       [],
        'config':       [],
        'relacionados': [],
    }

def _datos() -> dict:
    """Retorna los datos (Supabase o fallback)."""
    d = _cargar_datos_supabase()
    return d if d is not None else _fallback()


# ─────────────────────────────────────────────────────────
# API PÚBLICA — idéntica a constantes.py
# ─────────────────────────────────────────────────────────

def get_preguntas_intereses() -> list:
    return [p for p in _datos()['preguntas'] if p['tipo'] == 'interes']

def get_preguntas_habilidades() -> list:
    return [p for p in _datos()['preguntas'] if p['tipo'] == 'habilidad']

def get_knowledge_base() -> list[tuple]:
    """Retorna lista de (carrera, interes, habilidad) — igual que KNOWLEDGE_BASE."""
    return [(r['carrera'], r['interes'], r['habilidad']) for r in _datos()['reglas']]

def get_metadata_carreras() -> dict:
    """Retorna {nombre: {descripcion, area, color}} — igual que METADATA_CARRERAS."""
    return {
        c['nombre']: {
            'descripcion': c.get('descripcion', ''),
            'area':        c.get('area', ''),
            'color':       c.get('color', '#6B7280'),
        }
        for c in _datos()['carreras']
    }

def get_requisitos_carreras() -> dict:
    """Retorna {carrera: (interes, habilidad)} — igual que REQUISITOS_CARRERAS."""
    return {r['carrera']: (r['interes'], r['habilidad']) for r in _datos()['reglas']}

def get_intereses_relacionados() -> dict:
    """Retorna {interes: [relacionados]} — igual que INTERESES_RELACIONADOS."""
    resultado: dict[str, list] = {}
    for row in _datos()['relacionados']:
        resultado.setdefault(row['interes'], []).append(row['relacionado'])
    return resultado

def get_config() -> dict:
    """Retorna {clave: valor} para el algoritmo."""
    return {r['clave']: float(r['valor_numerico']) for r in _datos()['config']}

def get_id_a_categoria_interes() -> dict:
    return {p['id']: p['categoria'] for p in get_preguntas_intereses()}

def get_id_a_categoria_habilidad() -> dict:
    return {p['id']: p['categoria'] for p in get_preguntas_habilidades()}

def get_id_a_texto_pregunta() -> dict:
    todas = get_preguntas_intereses() + get_preguntas_habilidades()
    return {p['id']: p['texto'][:80] + '…' for p in todas}
