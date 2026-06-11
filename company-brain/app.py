from fastapi import FastAPI
import json

app = FastAPI()

with open("knowledge.json") as f:
    knowledge = json.load(f)

@app.get("/")
def home():
    return {
        "project": "Company Brain",
        "version": "1.0"
    }

@app.get("/documents")
def documents():
    return knowledge

@app.get("/search")
def search(q: str):
    results = []

    for item in knowledge:
        if q.lower() in item["content"].lower():
            results.append(item)

    return results

@app.get("/health")
def health():
    return {"status": "healthy"}