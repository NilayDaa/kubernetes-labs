from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import numpy as np

app = FastAPI()

# Load model ONCE (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Knowledge base
documents = [
    {
        "id": 1,
        "title": "Vacation Policy",
        "content": "Employees receive 25 paid vacation days"
    },
    {
        "id": 2,
        "title": "Remote Work",
        "content": "Employees can work from home 3 days per week"
    },
    {
        "id": 3,
        "title": "Lunch Policy",
        "content": "Company provides free lunch on Fridays"
    }
]

# Precompute embeddings (important optimization)
doc_texts = [d["content"] for d in documents]
doc_embeddings = model.encode(doc_texts)

@app.get("/")
def home():
    return {
        "service": "Company Brain AI",
        "version": "Day 10"
    }

@app.get("/search")
def search(q: str):
    # Convert query → vector
    query_embedding = model.encode([q])[0]

    # Similarity scoring
    scores = np.dot(doc_embeddings, query_embedding)

    # Sort results
    top_indices = scores.argsort()[::-1]

    results = [documents[i] for i in top_indices]

    return {
        "query": q,
        "results": results[:3]
    }

@app.get("/health")
def health():
    return {"status": "healthy"}