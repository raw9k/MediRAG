from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.pipeline import answer_question


app = FastAPI(
    title="MediRAG API",
    description="Medical question answering API using RAG.",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
def root():
    return {
        "message": "MediRAG API is running"
    }


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    answer, sources = answer_question(request.question)

    return QuestionResponse(
        answer=answer,
        sources=sources,
    )