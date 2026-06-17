from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .datos import CARRERAS
from .logica import inferir_carreras_candidatas, clasificar_carreras

OPCIONES = {
    "intereses": [
        ("tecnologia", "Tecnología"),
        ("matematicas", "Matemáticas"),
        ("innovacion", "Innovación"),
        ("salud", "Salud"),
        ("biologia", "Biología"),
        ("investigacion", "Investigación"),
        ("justicia", "Justicia"),
        ("lectura", "Lectura"),
        ("debate", "Debate"),
        ("personas", "Trato con personas"),
        ("conducta", "Conducta humana"),
        ("negocios", "Negocios"),
        ("liderazgo", "Liderazgo"),
        ("organizacion", "Organización"),
        ("finanzas", "Finanzas"),
        ("numeros", "Números"),
        ("arte", "Arte"),
        ("dibujo", "Dibujo"),
        ("construccion", "Construcción"),
        ("infraestructura", "Infraestructura"),
        ("ensenanza", "Enseñanza"),
        ("redes_sociales", "Redes sociales"),
        ("servicio", "Servicio"),
        ("procesos", "Procesos"),
        ("idiomas", "Idiomas")
    ],
    "habilidades": [
        ("logica", "Lógica"),
        ("analisis", "Análisis"),
        ("resolucion_problemas", "Resolución de problemas"),
        ("memoria", "Memoria"),
        ("empatia", "Empatía"),
        ("disciplina", "Disciplina"),
        ("argumentacion", "Argumentación"),
        ("lectura", "Lectura"),
        ("comunicacion", "Comunicación"),
        ("escucha", "Escucha activa"),
        ("liderazgo", "Liderazgo"),
        ("planificacion", "Planificación"),
        ("orden", "Orden"),
        ("calculo", "Cálculo"),
        ("creatividad", "Creatividad"),
        ("espacial", "Visión espacial"),
        ("detalle", "Atención al detalle"),
        ("paciencia", "Paciencia"),
        ("negociacion", "Negociación")
    ],
    "estilos_trabajo": [
        ("oficina", "Oficina"),
        ("remoto", "Remoto"),
        ("proyectos", "Trabajo por proyectos"),
        ("campo", "Campo"),
        ("hospital", "Hospital"),
        ("presencial", "Presencial"),
        ("asesoria", "Asesoría"),
        ("consulta", "Consulta"),
        ("aula", "Aula")
    ]
}

@require_http_methods(["GET"])
def inicio(request):
    return render(request, "recommender/index.html", {
        "opciones": OPCIONES,
        "total_carreras": len(CARRERAS)
    })

@require_http_methods(["POST"])
def recomendar(request):
    perfil_usuario = {
        "intereses": request.POST.getlist("intereses"),
        "habilidades": request.POST.getlist("habilidades"),
        "estilos_trabajo": request.POST.getlist("estilos_trabajo")
    }

    candidatas_logicas = inferir_carreras_candidatas(perfil_usuario, CARRERAS)
    recomendaciones = clasificar_carreras(CARRERAS, perfil_usuario, candidatas_logicas)

    return render(request, "recommender/results.html", {
        "perfil": perfil_usuario,
        "recomendaciones": recomendaciones,
        "candidatas_logicas": candidatas_logicas,
        "total_carreras": len(CARRERAS)
    })
