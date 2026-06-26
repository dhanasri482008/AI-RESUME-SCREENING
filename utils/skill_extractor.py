def extract_skills(tokens, skills_file="skills/skills.txt"):
    # Read skills from file
    with open(skills_file, "r", encoding="utf-8") as f:
        skills = [skill.strip().lower() for skill in f if skill.strip()]

    token_set = set(tokens)
    text = " ".join(tokens)

    found_skills = []

    for skill in skills:
        # Multi-word skills
        if " " in skill:
            if skill in text:
                found_skills.append(skill)
        else:
            if skill in token_set:
                found_skills.append(skill)

    return sorted(list(set(found_skills)))