from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.schemas import BlueprintCreate, BlueprintResponse
from app.services.blueprint_service import BlueprintService
from app.services.idea_service import IdeaService
from app.database import get_session
from app.routes.auth import get_current_user

router = APIRouter()

@router.post("", response_model=UUID)
async def create_blueprint(data: BlueprintCreate, session=Depends(get_session), user_id: UUID = Depends(get_current_user)):
    idea_service = IdeaService(session)
    idea = await idea_service.get(data.idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    service = BlueprintService(session)
    blueprint_id = await service.generate(data.idea_id, data.scope)
    return blueprint_id

@router.get("/{blueprint_id}", response_model=BlueprintResponse)
async def get_blueprint(blueprint_id: UUID, session=Depends(get_session), user_id: UUID = Depends(get_current_user)):
    service = BlueprintService(session)
    blueprint = await service.repo.get(blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return BlueprintResponse(id=blueprint.id, features=blueprint.features, timeline=blueprint.timeline)
