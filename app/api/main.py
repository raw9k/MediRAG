from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

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
    question: str = Field(
        ...,
        min_length=3,
        description="Medical question from the user.",
    )

    history: list[ChatMessage] = Field(
        default_factory=list,
        description="Previous conversation messages.",
    )


class QuestionResponse(BaseModel):
    answer: str
    sources: list[str]


# -------------------------
# Frontend routes
# -------------------------

@app.get("/")
def root():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/chat")
def chat_page():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# -------------------------
# API routes
# -------------------------

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        ]

        answer, sources = answer_question(
            question=request.question,
            history=history,
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