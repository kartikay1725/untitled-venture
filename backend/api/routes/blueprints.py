from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.blueprint import BlueprintCreate, BlueprintOut
from ..database import get_db
from ..services.blueprint_service import BlueprintService
from ..main import get_current_user

router = APIRouter()

@router.post("", response_model=BlueprintOut, status_code=status.HTTP_201_CREATED)
async def generate_blueprint(blueprint_in: BlueprintCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = BlueprintService(db)
    blueprint = await service.create_blueprint(blueprint_in, current_user.id)
    return blueprint

@router.get("/{blueprint_id}", response_model=BlueprintOut)
async def get_blueprint(blueprint_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = BlueprintService(db)
    blueprint = await service.get_blueprint(blueprint_id, current_user.id)
    if not blueprint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blueprint not found")
    return blueprint
