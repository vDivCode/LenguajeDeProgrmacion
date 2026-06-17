from functools import reduce

def intersection_score(selected_values, career_values, weight):
    return len(set(selected_values).intersection(set(career_values))) * weight

def calculate_score(career, user_profile, logical_candidates):
    interest_score = intersection_score(user_profile["interests"], career["interests"], 4)
    skill_score = intersection_score(user_profile["skills"], career["skills"], 3)
    style_score = intersection_score(user_profile["work_styles"], career["work_styles"], 2)
    logical_bonus = 5 if career["id"] in logical_candidates else 0

    total_score = reduce(
        lambda accumulated, current: accumulated + current,
        [interest_score, skill_score, style_score, logical_bonus],
        0
    )

    return {
        **career,
        "score": total_score,
        "matches": {
            "interests": list(set(user_profile["interests"]).intersection(career["interests"])),
            "skills": list(set(user_profile["skills"]).intersection(career["skills"])),
            "work_styles": list(set(user_profile["work_styles"]).intersection(career["work_styles"])),
            "logical_inference": career["id"] in logical_candidates
        }
    }

def rank_careers(careers, user_profile, logical_candidates, limit=5):
    scored_careers = list(map(
        lambda career: calculate_score(career, user_profile, logical_candidates),
        careers
    ))

    relevant_careers = list(filter(lambda career: career["score"] > 0, scored_careers))

    return sorted(
        relevant_careers,
        key=lambda career: career["score"],
        reverse=True
    )[:limit]
