from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def home():
    return {
        "app_name": os.getenv("APP_NAME"),
        "environment": os.getenv("ENVIRONMENT")
    }

@app.get("/health")
def health():
    return {"status": "healthy"}