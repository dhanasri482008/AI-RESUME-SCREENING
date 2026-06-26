from utils.preprocess import clean_resume
from utils.nlp_pipeline import preprocess_nlp
from utils.skill_extractor import extract_skills

def parse_job(job_file):
    with open(job_file, "r", encoding="utf-8") as f:
        text = f.read()

    cleaned = clean_resume(text)
    tokens = preprocess_nlp(cleaned)
    skills = extract_skills(tokens)

    return {
        "text": cleaned,
        "tokens": tokens,
        "skills": skills
    }