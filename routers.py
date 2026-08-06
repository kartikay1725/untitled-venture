from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from .database import get_session
from .auth_service import create_user, authenticate_user, create_access_token, get_current_user
from .schemas import UserCreate, Token, IdeaCreate, IdeaResponse, ValidationResponse, BlueprintCreate, BlueprintResponse
from .idea_service import create_idea, get_idea_validation
from .blueprint_service import generate_blueprint
from .models import User, MVPBlueprint

router = APIRouter()

@router.post("/auth/register", response_model=Token)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.execute(select(User).where(User.email == user_in.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(session, user_in.email, user_in.password)
    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)

@router.post("/auth/login", response_model=Token)
async def login(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(session, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)

@router.post("/ideas", response_model=IdeaResponse)
async def submit_idea(idea_in: IdeaCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    idea = await create_idea(session, current_user.id, idea_in)
    return IdeaResponse.from_orm(idea)

@router.get("/ideas/{idea_id}/validation", response_model=ValidationResponse)
async def get_validation(idea_id: uuid.UUID, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    idea = await get_idea_validation(session, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return ValidationResponse(
        validation_score=float(idea.validation_score) if idea.validation_score else None,
        validation_feedback=idea.validation_feedback,
        status=idea.status.value
    )

@router.post("/blueprints", response_model=BlueprintResponse)
async def create_blueprint(blueprint_in: BlueprintCreate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    idea = await get_idea_validation(session, blueprint_in.idea_id)
    if not idea or idea.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Idea not found or not owned")
    blueprint = await generate_blueprint(session, blueprint_in)
    return BlueprintResponse.from_orm(blueprint)

@router.get("/blueprints/{blueprint_id}", response_model=BlueprintResponse)
async def get_blueprint(blueprint_id: uuid.UUID, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(MVPBlueprint).where(MVPBlueprint.id == blueprint_id))
    blueprint = result.scalar_one_or_none()
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    if blueprint.idea.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return BlueprintResponse.from_orm(blueprint)
