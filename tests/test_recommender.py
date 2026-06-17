from recommender.data.careers import CAREERS
from recommender.logic_rules.rules import infer_candidate_careers
from recommender.processor.recommender import rank_careers

def test_recommends_systems_first_for_technology_profile():
    profile = {
        "interests": ["tecnologia", "matematicas", "innovacion"],
        "skills": ["logica", "analisis", "resolucion_problemas"],
        "work_styles": ["remoto", "proyectos"]
    }

    logical_candidates = infer_candidate_careers(profile, CAREERS)
    ranking = rank_careers(CAREERS, profile, logical_candidates)

    assert ranking
    assert ranking[0]["id"] == "sistemas"

def test_recommends_health_area_for_health_profile():
    profile = {
        "interests": ["salud", "personas", "servicio"],
        "skills": ["empatia", "disciplina", "paciencia"],
        "work_styles": ["hospital", "presencial"]
    }

    logical_candidates = infer_candidate_careers(profile, CAREERS)
    ranking = rank_careers(CAREERS, profile, logical_candidates)

    assert ranking
    assert ranking[0]["area"] == "Salud"

def test_knowledge_base_has_minimum_ten_items():
    assert len(CAREERS) >= 10
