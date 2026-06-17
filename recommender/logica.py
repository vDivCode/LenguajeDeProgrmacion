from pyDatalog import pyDatalog

# Configuración de pyDatalog
pyDatalog.create_terms(
    "interes_carrera, habilidad_carrera, estilo_carrera, le_gusta, tiene_habilidad, "
    "prefiere_estilo, candidato, C, I, S, W"
)

def cargar_base_conocimiento(carreras):
    pyDatalog.clear()
    pyDatalog.create_terms(
        "interes_carrera, habilidad_carrera, estilo_carrera, le_gusta, tiene_habilidad, "
        "prefiere_estilo, candidato, C, I, S, W"
    )

    for carrera in carreras:
        for interes in carrera["intereses"]:
            +interes_carrera(carrera["id"], interes)

        for habilidad in carrera["habilidades"]:
            +habilidad_carrera(carrera["id"], habilidad)

        for estilo in carrera["estilos_trabajo"]:
            +estilo_carrera(carrera["id"], estilo)

    candidato(C) <= (le_gusta(I) & interes_carrera(C, I))
    candidato(C) <= (tiene_habilidad(S) & habilidad_carrera(C, S))
    candidato(C) <= (prefiere_estilo(W) & estilo_carrera(C, W))

def inferir_carreras_candidatas(perfil_usuario, carreras):
    cargar_base_conocimiento(carreras)

    for interes in perfil_usuario.get("intereses", []):
        +le_gusta(interes)

    for habilidad in perfil_usuario.get("habilidades", []):
        +tiene_habilidad(habilidad)

    for estilo in perfil_usuario.get("estilos_trabajo", []):
        +prefiere_estilo(estilo)

    resultado = candidato(C)
    return sorted({str(fila[0]) for fila in resultado})

# Lógica de Puntaje y Clasificación
def puntaje_interseccion(valores_seleccionados, valores_carrera, peso):
    return len(set(valores_seleccionados).intersection(set(valores_carrera))) * peso

def calcular_puntaje(carrera, perfil_usuario, candidatas_logicas):
    puntaje_interes = puntaje_interseccion(perfil_usuario["intereses"], carrera["intereses"], 4)
    puntaje_habilidad = puntaje_interseccion(perfil_usuario["habilidades"], carrera["habilidades"], 3)
    puntaje_estilo = puntaje_interseccion(perfil_usuario["estilos_trabajo"], carrera["estilos_trabajo"], 2)
    bono_logico = 5 if carrera["id"] in candidatas_logicas else 0

    puntaje_total = puntaje_interes + puntaje_habilidad + puntaje_estilo + bono_logico

    return {
        **carrera,
        "puntaje": puntaje_total,
        "coincidencias": {
            "intereses": list(set(perfil_usuario["intereses"]).intersection(carrera["intereses"])),
            "habilidades": list(set(perfil_usuario["habilidades"]).intersection(carrera["habilidades"])),
            "estilos_trabajo": list(set(perfil_usuario["estilos_trabajo"]).intersection(carrera["estilos_trabajo"])),
            "inferencia_logica": carrera["id"] in candidatas_logicas
        }
    }

def clasificar_carreras(carreras, perfil_usuario, candidatas_logicas, limite=5):
    carreras_con_puntaje = [
        calcular_puntaje(carrera, perfil_usuario, candidatas_logicas)
        for carrera in carreras
    ]

    carreras_relevantes = [c for c in carreras_con_puntaje if c["puntaje"] > 0]

    return sorted(
        carreras_relevantes,
        key=lambda c: c["puntaje"],
        reverse=True
    )[:limite]
