from sentence_transformers import SentenceTransformer
import numpy as np

# 1. Load model (small + fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Your knowledge base
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

# 3. Convert documents → vectors
doc_texts = [d["content"] for d in documents]
doc_embeddings = model.encode(doc_texts)

def search(query, top_k=2):
    # Convert query → vector
    query_embedding = model.encode([query])[0]

    # Similarity (dot product)
    scores = np.dot(doc_embeddings, query_embedding)

    # Get best matches
    top_indices = scores.argsort()[::-1][:top_k]

    return [documents[i] for i in top_indices]


# 4. Interactive testing
while True:
    q = input("\nSearch: ")
    results = search(q)

    print("\nResults:")
    for r in results:
        print("-", r["title"], ":", r["content"])