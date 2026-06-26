from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(job_text, resume_text):
    job_embedding = model.encode([job_text])
    resume_embedding = model.encode([resume_text])

    score = cosine_similarity(job_embedding, resume_embedding)[0][0]

    return round(score * 100, 2)