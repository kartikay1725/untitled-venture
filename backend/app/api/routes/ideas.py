from fastapi import APIRouter, Depends, HTTPException, status
from ...services.idea_service import IdeaService
from ...services.validation_service import ValidationService
from ...api.schemas import IdeaCreateRequest, IdeaResponse, ValidationResponse
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

@router.post("/", response_model=IdeaResponse)
async def submit_idea(req: IdeaCreateRequest, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/login"))):
    user_id = UserService.get_user_id_from_token(token)
    return await IdeaService.create_idea(user_id, req.title, req.description)

@router.get("/{idea_id}/validation", response_model=ValidationResponse)
async def get_validation(idea_id: UUID, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/login"))):
    return await ValidationService.get_validation(idea_id)
