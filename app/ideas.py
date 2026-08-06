from fastapi import APIRouter, Depends, HTTPException
from .schemas import IdeaRequest, IdeaResponse, ValidationResponse
from .models import Idea
from .database import get_session
from sqlmodel import select, Session
from uuid import UUID
from .security import decode_token
from .engine.validation_service import validate_idea
import logging

router = APIRouter(prefix="/ideas", tags=["ideas"])
logger = logging.getLogger(__name__)

def get_current_user_id(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return payload["sub"]

@router.post("/", response_model=IdeaResponse)
async def submit_idea(request: IdeaRequest, user_id: str = Depends(get_current_user_id)):
    async with get_session() as session:
        idea = Idea(user_id=user_id, title=request.title, description=request.description)
        session.add(idea)
        await session.commit()
        await session.refresh(idea)
    logger.info(f"Idea submitted by user {user_id}: {idea.id}")
    return IdeaResponse(
        id=idea.id,
        title=idea.title,
        description=idea.description,
        submitted_at=idea.submitted_at,
        validation_score=idea.validation_score,
        validation_feedback=idea.validation_feedback,
        status=idea.status
    )

@router.get("/{idea_id}/validation", response_model=ValidationResponse)
async def get_validation(idea_id: UUID, user_id: str = Depends(get_current_user_id)):
    async with get_session() as session:
        idea = await session.get(Idea, idea_id)
        if not idea or idea.user_id != user_id:
            raise HTTPException(status_code=404, detail="Idea not found")
        if idea.status == "pending":
            score, feedback = await validate_idea(idea.title, idea.description)
            idea.validation_score = score
            idea.validation_feedback = feedback
            idea.status = "validated"
            await session.commit()
        return ValidationResponse(
            validation_score=idea.validation_score,
            validation_feedback=idea.validation_feedback,
            status=idea.status
        )
