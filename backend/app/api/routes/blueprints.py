from fastapi import APIRouter, Depends, HTTPException
from ...services.blueprint_service import BlueprintService
from ...api.schemas import BlueprintCreateRequest, BlueprintResponse
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

@router.post("/", response_model=BlueprintResponse)
async def generate_blueprint(req: BlueprintCreateRequest, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/login"))):
    return await BlueprintService.generate_blueprint(req.idea_id, req.scope)

@router.get("/{blueprint_id}", response_model=BlueprintResponse)
async def get_blueprint(blueprint_id: UUID, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/login"))):
    return await BlueprintService.get_blueprint(blueprint_id)
