from fastapi import APIRouter, HTTPException

from backend.app.schemas.chat import AskRequest, AskResponse
from backend.app.services.rag_service import ask_question


router = APIRouter(tags=["Chat"])


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        return ask_question(request.question)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process legal question: {str(exc)}",
        )