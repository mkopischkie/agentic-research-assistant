# backend/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI(title="Agentic Research Assistant")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "openai_key_set": bool(os.getenv("OPENAI_API_KEY")),
        "db_url_set": bool(os.getenv("DATABASE_URL")),
    }