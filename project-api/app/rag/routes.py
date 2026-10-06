from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.config import PDF_DIR
from app.rag.service import answer_question, start_interview, submit_answer

router = APIRouter(tags=["DevOps Knowledge Agent"])


class StartRequest(BaseModel):
    document: str | None = Field(
        default=None,
        description="Optional PDF filename, for example devops-notes.pdf",
    )


class AnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=10000)


class QARequest(BaseModel):
    question: str = Field(min_length=1, max_length=5000)
    document: str | None = Field(
        default=None,
        description="Optional PDF filename, for example devops-notes.pdf",
    )


@router.post(
    "/ask",
    summary="Ask a DevOps question",
    description="Answer a DevOps question using the indexed PDF knowledge base.",
)
def ask(request: QARequest):
    if request.document:
        if "/" in request.document or "\\" in request.document:
            raise HTTPException(status_code=400, detail="Provide a PDF filename only")
        if not request.document.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Document must be a PDF")
        if not (PDF_DIR / request.document).is_file():
            raise HTTPException(status_code=404, detail="PDF not found in data/pdfs")

    try:
        answer = answer_question(request.question, request.document)
        return {"answer": answer}
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post(
    "/start",
    summary="Start interview session",
    description="Generate a troubleshooting question from the knowledge base.",
)
def start(request: StartRequest):
    if request.document:
        if "/" in request.document or "\\" in request.document:
            raise HTTPException(status_code=400, detail="Provide a PDF filename only")
        if not request.document.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Document must be a PDF")
        if not (PDF_DIR / request.document).is_file():
            raise HTTPException(status_code=404, detail="PDF not found in data/pdfs")

    try:
        session_id, question = start_interview(request.document)
        return {"session_id": session_id, "question": question}
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post(
    "/{session_id}/answer",
    summary="Submit interview answer",
    description="Evaluate a candidate answer against the DevOps knowledge base.",
)
def answer(session_id: str, request: AnswerRequest):
    try:
        feedback = submit_answer(session_id, request.answer)
        return {"feedback": feedback}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
