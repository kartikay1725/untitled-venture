from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..db import get_db
from ..models import Idea
from sqlalchemy.orm import Session
import uuid
from ..utils.security import decode_token
from datetime import datetime

router = APIRouter()

class IdeaRequest(BaseModel):
    description: str

class IdeaResponse(BaseModel):
    idea_id: uuid.UUID
    validation_score: Optional[float]
    validated_at: Optional[datetime]

# Simple token extractor
async def get_current_user(token: str = Depends(lambda request: request.headers.get("Authorization", "").split(" ")[1]), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

@router.post("/", response_model=IdeaResponse)
def submit_idea(payload: IdeaRequest, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user)):
    idea = Idea(id=uuid.uuid4(), user_id=user_id, description=payload.description)
    db.add(idea)
    db.commit()
    db.refresh(idea)
    # Mock validation logic
    score = 0.75 if "app" in payload.description.lower() else 0.65
    idea.validation_score = score
    idea.validated_at = datetime.utcnow()
    db.commit()
    db.refresh(idea)
    return IdeaResponse(idea_id=idea.id, validation_score=idea.validation_score, validated_at=idea.validated_at)

@router.get("/{idea_id}/validation", response_model=IdeaResponse)
def get_validation(idea_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user)):
    idea = db.query(Idea).filter(Idea.id == idea_id, Idea.user_id == user_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return IdeaResponse(idea_id=idea.id, validation_score=idea.validation_score, validated_at=idea.validated_at)