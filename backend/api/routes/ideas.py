from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.idea import IdeaCreate, IdeaOut
from ..database import get_db
from ..services.idea_service import IdeaService
from ..services.validation_service import ValidationService
from ..main import get_current_user

router = APIRouter()

@router.post("", response_model=IdeaOut, status_code=status.HTTP_201_CREATED)
async def submit_idea(idea_in: IdeaCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = IdeaService(db)
    idea = await service.create_idea(idea_in, current_user.id)
    # Trigger async validation
    validator = ValidationService(db)
    await validator.validate_idea(idea.id)
    return idea

@router.get("/{idea_id}/validation", response_model=IdeaOut)
async def get_validation(idea_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = IdeaService(db)
    idea = await service.get_idea(idea_id, current_user.id)
    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idea not found")
    return idea
