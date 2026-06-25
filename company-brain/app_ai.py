from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import numpy as np
import os

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
        "version": os.getenv("APP_VERSION", "Day 10"),
        "service": os.getenv("SERVICE_NAME", "Company Brain AI")
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


@app.get("/config")
def config():
    return {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }

@app.get("/secret-files")
def secret_files():
    with open("/app/secrets/DB_USER", "r") as f:
        user = f.read().strip()

    with open("/app/secrets/DB_PASSWORD", "r") as f:
        password = f.read().strip()

    return {
        "user": user,
        "password": password
    }