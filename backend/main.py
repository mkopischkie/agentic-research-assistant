# backend/main.py
from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
import os

from agent import answer
from retriever import add_to_storage

load_dotenv()
app = FastAPI(title="Agentic Research Assistant")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "openai_key_set": bool(os.getenv("OPENAI_API_KEY")),
        "db_url_set": bool(os.getenv("DATABASE_URL")),
    }

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/uploads"))
@app.post("/uploads")
async def upload(file: UploadFile = File(...)):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename or "upload").name   # strip path traversal
    dest = UPLOAD_DIR / safe_name
    dest.write_bytes(await file.read())
    add_to_storage(str(dest))   # ingest -> chunk -> embed -> store so answer() can retrieve it
    return {"success": True, "filename": safe_name}


class AskRequest(BaseModel):
    query: str


@app.post("/ask")
def ask(req: AskRequest):
    return answer(req.query)   # {"answer", "citations", "context"}