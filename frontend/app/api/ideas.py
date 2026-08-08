"""Idea submission and validation routes.

POST /api/ideas creates an idea record and returns validation score.
GET /api/ideas/{idea_id}/validation retrieves the score.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models import Idea
from app.services.idea_validation_service import validate_idea

router = APIRouter()

class IdeaRequest(BaseModel):
    description: str

class IdeaResponse(BaseModel):
    idea_id: str
    validation_score: float
    validated_at: str

@router.post("", response_model=IdeaResponse)
async def submit_idea(req: IdeaRequest, db: Session = Depends(get_db)):
    score = validate_idea(req.description)
    idea = Idea(description=req.description, validation_score=score)
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return IdeaResponse(
        idea_id=str(idea.id),
        validation_score=idea.validation_score,
        validated_at=idea.validated_at.isoformat(),
    )

@router.get("/{idea_id}/validation", response_model=IdeaResponse)
async def get_validation(idea_id: str, db: Session = Depends(get_db)):
    idea = db.query(Idea).filter(Idea.id == uuid.UUID(idea_id)).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return IdeaResponse(
        idea_id=str(idea.id),
        validation_score=idea.validation_score,
        validated_at=idea.validated_at.isoformat(),
    )