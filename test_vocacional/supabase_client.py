"""
=============================================================================
MÓDULO SUPABASE - supabase_client.py
=============================================================================
Cliente de Supabase para guardar usuarios y resultados del test vocacional.
=============================================================================
"""

import os
import logging

logger = logging.getLogger(__name__)

# Intentamos importar supabase; si no está instalado, lo indicamos claramente
try:
    from supabase import create_client, Client
    _SUPABASE_DISPONIBLE = True
except ImportError:
    _SUPABASE_DISPONIBLE = False
    logger.warning("Librería 'supabase' no instalada. Ejecuta: pip install supabase")


def get_client():
    """
    Retorna el cliente de Supabase configurado.
    Retorna None si las credenciales no están configuradas.
    """
    if not _SUPABASE_DISPONIBLE:
        return None

    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_ANON_KEY", "")

    if not url or not key or "xxxxxx" in url:
        logger.warning(
            "Supabase no configurado. Rellena SUPABASE_URL y SUPABASE_ANON_KEY en .env"
        )
        return None

    try:
        return create_client(url, key)
    except Exception as exc:
        logger.error("Error al crear cliente Supabase: %s", exc)
        return None


def guardar_usuario(nombre: str, email: str = "", edad: int = None, pais: str = "Perú") -> str | None:
    """
    Inserta un nuevo usuario en la tabla usuarios_test.
    Retorna el UUID del usuario creado, o None si falla.
    """
    client = get_client()
    if client is None:
        return None

    datos = {
        "nombre": nombre.strip(),
        "pais": pais or "Perú",
    }
    if email and email.strip():
        datos["email"] = email.strip().lower()
    if edad and str(edad).isdigit():
        datos["edad"] = int(edad)

    try:
        respuesta = client.table("usuarios_test").insert(datos).execute()
        if respuesta.data:
            usuario_id = respuesta.data[0]["id"]
            logger.info("Usuario creado: %s (id=%s)", nombre, usuario_id)
            return usuario_id
    except Exception as exc:
        logger.error("Error al guardar usuario en Supabase: %s", exc)

    return None


def guardar_resultado(usuario_id: str | None, resultado: dict) -> bool:
    """
    Inserta el resultado del test en la tabla resultados_test.
    Retorna True si se guardó correctamente, False si no.
    """
    client = get_client()
    if client is None:
        return False

    recomendaciones = resultado.get("recomendaciones", [])
    perfil          = resultado.get("perfil", {})

    # Carrera top = primera recomendación
    carrera_top  = recomendaciones[0].get("carrera", "") if recomendaciones else ""
    puntaje_top  = recomendaciones[0].get("puntaje_ponderado", 0) if recomendaciones else 0

    datos = {
        "carrera_top":         carrera_top,
        "puntaje_top":         round(float(puntaje_top), 2),
        "total_candidatas":    resultado.get("total_candidatas_logicas", 0),
        "recomendaciones":     recomendaciones,
        "perfil_intereses":    perfil.get("intereses", {}),
        "perfil_habilidades":  perfil.get("habilidades", {}),
        "advertencias":        resultado.get("advertencias", []),
    }

    if usuario_id:
        datos["usuario_id"] = usuario_id

    try:
        respuesta = client.table("resultados_test").insert(datos).execute()
        if respuesta.data:
            logger.info("Resultado guardado en Supabase para carrera: %s", carrera_top)
            return True
    except Exception as exc:
        logger.error("Error al guardar resultado en Supabase: %s", exc)

    return False
