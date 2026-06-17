from recommender.datos import CARRERAS
from recommender.logica import inferir_carreras_candidatas, clasificar_carreras

def test_recomienda_sistemas_primero_para_perfil_tecnologico():
    perfil = {
        "intereses": ["tecnologia", "matematicas", "innovacion"],
        "habilidades": ["logica", "analisis", "resolucion_problemas"],
        "estilos_trabajo": ["remoto", "proyectos"]
    }

    candidatas_logicas = inferir_carreras_candidatas(perfil, CARRERAS)
    clasificacion = clasificar_carreras(CARRERAS, perfil, candidatas_logicas)

    assert clasificacion
    assert clasificacion[0]["id"] == "sistemas"

def test_recomienda_area_salud_para_perfil_saludable():
    perfil = {
        "intereses": ["salud", "personas", "servicio"],
        "habilidades": ["empatia", "disciplina", "paciencia"],
        "estilos_trabajo": ["hospital", "presencial"]
    }

    candidatas_logicas = inferir_carreras_candidatas(perfil, CARRERAS)
    clasificacion = clasificar_carreras(CARRERAS, perfil, candidatas_logicas)

    assert clasificacion
    assert clasificacion[0]["area"] == "Salud"

def test_base_conocimiento_tiene_minimo_diez_items():
    assert len(CARRERAS) >= 10
