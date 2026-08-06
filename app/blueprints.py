from fastapi import APIRouter, Depends, HTTPException
from .schemas import BlueprintRequest, BlueprintResponse
from .models import Blueprint, Idea
from .database import get_session
from sqlmodel import Session
from uuid import UUID
from .security import decode_token
from .engine.blueprint_service import generate_blueprint
import logging

router = APIRouter(prefix="/blueprints", tags=["blueprints"])
logger = logging.getLogger(__name__)

def get_current_user_id(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = auth_header.split(" ")[1]
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return payload["sub"]

@router.post("/", response_model=BlueprintResponse)
async def create_blueprint(req: BlueprintRequest, user_id: str = Depends(get_current_user_id)):
    async with get_session() as session:
        idea = await session.get(Idea, req.idea_id)
        if not idea or idea.user_id != user_id:
            raise HTTPException(status_code=404, detail="Idea not found")
        features, timeline = await generate_blueprint(idea.title, idea.description, req.scope)
        blueprint = Blueprint(idea_id=idea.id, features=features, timeline=timeline)
        session.add(blueprint)
        await session.commit()
        await session.refresh(blueprint)
    logger.info(f"Blueprint generated for idea {req.idea_id}")
    return BlueprintResponse(
        id=blueprint.id,
        features=blueprint.features,
        timeline=blueprint.timeline,
        created_at=blueprint.created_at
    )

@router.get("/{blueprint_id}", response_model=BlueprintResponse)
async def get_blueprint(blueprint_id: UUID, user_id: str = Depends(get_current_user_id)):
    async with get_session() as session:
        blueprint = await session.get(Blueprint, blueprint_id)
        if not blueprint:
            raise HTTPException(status_code=404, detail="Blueprint not found")
        idea = await session.get(Idea, blueprint.idea_id)
        if idea.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
    return BlueprintResponse(
        id=blueprint.id,
        features=blueprint.features,
        timeline=blueprint.timeline,
        created_at=blueprint.created_at
    )
