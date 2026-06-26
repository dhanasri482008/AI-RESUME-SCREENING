import pandas as pd

from utils.preprocess import clean_resume
from utils.nlp_pipeline import preprocess_nlp
from utils.skill_extractor import extract_skills
from utils.matcher import match_skills
from utils.similarity import semantic_similarity
from utils.scorer import final_score


def rank_resumes(df, job):

    results = []

    for _, row in df.iterrows():

        # Resume Text
        resume = row["Resume_html"]

        cleaned_resume = clean_resume(resume)

        # NLP
        tokens = preprocess_nlp(cleaned_resume)

        # Skills
        resume_skills = extract_skills(tokens)

        # Skill Match
        match = match_skills(
            job["skills"],
            resume_skills
        )

        # Semantic Similarity
        similarity = semantic_similarity(
            job["text"],
            cleaned_resume
        )

        # Final Score
        score = final_score(
            match["score"],
            similarity
        )

        results.append({
            "ID": row["ID"],
            "Category": row["Category"],
            "Skill Score": match["score"],
            "Semantic Score": round(similarity, 2),
            "Final Score": score
        })

    ranked = pd.DataFrame(results)

    ranked = ranked.sort_values(
        by="Final Score",
        ascending=False
    )

    ranked.reset_index(drop=True, inplace=True)

    ranked.index += 1

    return ranked