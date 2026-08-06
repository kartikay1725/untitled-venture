from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.schemas import IdeaCreate, IdeaResponse, ValidationResponse
from app.services.idea_service import IdeaService
from app.services.validation_service import ValidationService
from app.database import get_session
from app.routes.auth import get_current_user

router = APIRouter()

@router.post("", response_model=IdeaResponse)
async def submit_idea(data: IdeaCreate, session=Depends(get_session), user_id: UUID = Depends(get_current_user)):
    service = IdeaService(session)
    idea_id = await service.submit(user_id, data)
    idea = await service.get(idea_id)
    return IdeaResponse(**idea.__dict__)

@router.get("/{idea_id}/validation", response_model=ValidationResponse)
async def get_validation(idea_id: UUID, session=Depends(get_session), user_id: UUID = Depends(get_current_user)):
    service = ValidationService(session)
    try:
        score, feedback = await service.validate(idea_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return ValidationResponse(validation_score=score, validation_feedback=feedback, status="validated")
