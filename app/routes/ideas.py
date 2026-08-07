from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import async_session
from app.models import Idea
from app.schemas import IdeaCreate, IdeaOut, ValidationResult
from app.services.validation_service import ValidationService
from app.utils.security import get_current_user
import uuid
import logging

router = APIRouter()

@router.post("/", response_model=IdeaOut)
async def create_idea(idea_in: IdeaCreate, token=Depends(get_current_user)):
    async with async_session() as session:
        idea = Idea(
            id=uuid.uuid4(),
            user_id=token.user_id,
            description=idea_in.description,
            industry_tags=idea_in.industry_tags
        )
        session.add(idea)
        await session.commit()
        await session.refresh(idea)
        service = ValidationService()
        score, text, features = await service.validate(idea.description, idea.industry_tags)
        idea.validation_score = score
        idea.validation_text = text
        idea.recommended_features = features
        await session.commit()
        await session.refresh(idea)
        return IdeaOut.from_orm(idea)

@router.get("/{idea_id}/validation", response_model=ValidationResult)
async def get_validation(idea_id: uuid.UUID, token=Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(select(Idea).where(Idea.id == idea_id, Idea.user_id == token.user_id))
        idea = result.scalars().first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        if idea.validation_score is None:
            raise HTTPException(status_code=202, detail="Validation pending")
        return ValidationResult(
            validationScore=float(idea.validation_score),
            validationText=idea.validation_text,
            recommendedFeatures=idea.recommended_features
        )
