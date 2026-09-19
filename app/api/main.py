from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.rag.pipeline import answer_question

app = FastAPI(
    title="MediRAG API",
    description="Medical question answering API using RAG.",
    version="1.0.0",
)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

class ChatMessage(BaseModel):
    role: str
    content: str


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=3)
    history: list[ChatMessage] = []


class QuestionResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
def root():
    return {"message": "MediRAG API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/chat")
def chat_page():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        answer, sources = answer_question(
            question=request.question,
            history=[
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in request.history
            ],
        )

        return QuestionResponse(
            answer=answer,
            sources=sources,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(e)}",
        )