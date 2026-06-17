from pyDatalog import pyDatalog

pyDatalog.create_terms(
    "career_interest, career_skill, career_style, likes, has_skill, "
    "prefers_style, candidate, C, I, S, W"
)

def load_knowledge_base(careers):
    pyDatalog.clear()
    pyDatalog.create_terms(
        "career_interest, career_skill, career_style, likes, has_skill, "
        "prefers_style, candidate, C, I, S, W"
    )

    for career in careers:
        for interest in career["interests"]:
            +career_interest(career["id"], interest)

        for skill in career["skills"]:
            +career_skill(career["id"], skill)

        for style in career["work_styles"]:
            +career_style(career["id"], style)

    candidate(C) <= (likes(I) & career_interest(C, I))
    candidate(C) <= (has_skill(S) & career_skill(C, S))
    candidate(C) <= (prefers_style(W) & career_style(C, W))

def infer_candidate_careers(user_profile, careers):
    load_knowledge_base(careers)

    for interest in user_profile.get("interests", []):
        +likes(interest)

    for skill in user_profile.get("skills", []):
        +has_skill(skill)

    for style in user_profile.get("work_styles", []):
        +prefers_style(style)

    result = candidate(C)
    return sorted({str(row[0]) for row in result})
