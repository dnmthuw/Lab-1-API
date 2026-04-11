import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.model import QuestionAnsweringModel


_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONFIG_PATH = os.path.join(_BASE_DIR, "config", "config.yaml")

app = FastAPI(
    title="Question Answering API",
    description="QA API using DistilBERT to answer questions from a predefined dataset.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise model 
qa_model = QuestionAnsweringModel(_CONFIG_PATH)

class QuestionInput(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "system": "LAB 1: Question Answering API",
        "model": "distilbert-base-cased-distilled-squad",
        "description": (
            "The Question Answering API retrieves answers from a predefined "
            "dataset based on user queries and returns them in JSON format"
        ),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: QuestionInput):
    # ------------------------------------------------------------------
    # 400 — reject empty / whitespace-only questions before touching the model
    # ------------------------------------------------------------------
    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # ------------------------------------------------------------------
    # 500 — wrap inference in try-except so model errors surface cleanly
    # instead of returning an unhandled 500 traceback to the client.
    # ------------------------------------------------------------------
    try:
        answer = qa_model(data.question)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference error: {exc}",
        ) from exc

    return {
        "question": data.question,
        "answer": answer,
    }