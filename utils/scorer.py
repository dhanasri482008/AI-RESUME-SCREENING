def final_score(skill_score, semantic_score):
    """
    Final Score =
    40% Skill Match +
    60% Semantic Similarity
    """

    score = (0.4 * skill_score) + (0.6 * semantic_score)

    return round(score, 2)