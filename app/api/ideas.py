from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Idea, User
from app.utils.settings import Settings
from app.db import get_db, get_current_user
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

router = APIRouter()
settings = Settings()

class IdeaRequest(BaseModel):
    description: str

class IdeaResponse(BaseModel):
    idea_id: str
    validation_score: float
    validated_at: datetime

@router.post("", response_model=IdeaResponse)
async def submit_idea(req: IdeaRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    # Dummy validation logic: score = len(description) % 100
    score = min(100, max(0, len(req.description) % 100))
    idea = Idea(user_id=user.id, description=req.description, validation_score=score, validated_at=datetime.utcnow())
    db.add(idea)
    await db.commit()
    await db.refresh(idea)
    return IdeaResponse(idea_id=str(idea.id), validation_score=idea.validation_score, validated_at=idea.validated_at)

@router.get("{idea_id}/validation", response_model=IdeaResponse)
async def get_validation(idea_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Idea).where(Idea.id == idea_id, Idea.user_id == user.id))
    idea = result.scalar_one_or_none()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return IdeaResponse(idea_id=str(idea.id), validation_score=idea.validation_score, validated_at=idea.validated_at)
