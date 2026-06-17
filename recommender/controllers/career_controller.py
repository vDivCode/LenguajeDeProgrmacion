# pyrefly: ignore [missing-import]
from django.shortcuts import render
# pyrefly: ignore [missing-import]
from django.views.decorators.http import require_http_methods
# pyrefly: ignore [missing-import]
from django.utils.decorators import method_decorator

from recommender.data.careers import CAREERS
from recommender.logic_rules.rules import infer_candidate_careers
from recommender.processor.recommender import rank_careers

OPTIONS = {
    "interests": [
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
    "skills": [
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
    "work_styles": [
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

class CareerController:
    @method_decorator(require_http_methods(["GET"]))
    def index(self, request):
        return render(request, "recommender/index.html", {
            "options": OPTIONS,
            "total_careers": len(CAREERS)
        })

    @method_decorator(require_http_methods(["POST"]))
    def recommend(self, request):
        user_profile = {
            "interests": request.POST.getlist("interests"),
            "skills": request.POST.getlist("skills"),
            "work_styles": request.POST.getlist("work_styles")
        }

        logical_candidates = infer_candidate_careers(user_profile, CAREERS)
        recommendations = rank_careers(CAREERS, user_profile, logical_candidates)

        return render(request, "recommender/results.html", {
            "profile": user_profile,
            "recommendations": recommendations,
            "logical_candidates": logical_candidates,
            "total_careers": len(CAREERS)
        })
