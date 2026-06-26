import pandas as pd

from utils.preprocess import clean_resume
from utils.nlp_pipeline import preprocess_nlp
from utils.skill_extractor import extract_skills

df = pd.read_csv("dataset/Resume.csv")

resume = df["Resume_html"][0]

cleaned = clean_resume(resume)

tokens = preprocess_nlp(cleaned)

skills = extract_skills(tokens)

print("\nDetected Skills:\n")
print(skills)