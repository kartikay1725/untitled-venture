import uuid, logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from .models import User, Idea, Blueprint
from .ai import AIClient, ValidationResult, BlueprintResult
from datetime import datetime

logger = logging.getLogger("mvpgenie.services")

class ValidationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, email: str, password: str) -> User:
        user = User(id=uuid.uuid4(), email=email, password_hash=User.hash_password(password))
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate(self, email: str, password: str) -> Optional[str]:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if user and User.verify_password(password, user.password_hash):
            return user.generate_token()
        return None

    async def submit_idea(self, token: str, title: str, description: str) -> Idea:
        user = await self._get_user_from_token(token)
        idea = Idea(id=uuid.uuid4(), user_id=user.id, title=title, description=description, status="pending")
        self.db.add(idea)
        await self.db.commit()
        await self.db.refresh(idea)
        return idea

    async def get_validation(self, token: str, idea_id: uuid.UUID) -> Optional[ValidationResult]:
        idea = await self._get_idea(token, idea_id)
        if idea and idea.validation_score is not None:
            return ValidationResult(score=idea.validation_score, feedback=idea.validation_feedback)
        return None

    async def _get_user_from_token(self, token: str) -> User:
        stmt = select(User).where(User.token == token)
        result = await self.db.execute(stmt)
        user = result.scalar_one()
        return user

    async def _get_idea(self, token: str, idea_id: uuid.UUID) -> Idea:
        user = await self._get_user_from_token(token)
        stmt = select(Idea).where(Idea.id == idea_id, Idea.user_id == user.id)
        result = await self.db.execute(stmt)
        idea = result.scalar_one()
        return idea

class BlueprintService:
    def __init__(self, db: AsyncSession, ai_client: AIClient):
        self.db = db
        self.ai = ai_client

    async def create_blueprint(self, token: str, idea_id: uuid.UUID, scope: str) -> Blueprint:
        idea = await self._get_idea(token, idea_id)
        if idea.validation_score is None:
            raise ValueError("Idea not validated yet")
        blueprint_data = await self.ai.generate_blueprint(idea.title, idea.description, scope)
        blueprint = Blueprint(id=uuid.uuid4(), idea_id=idea.id, features=blueprint_data.features, timeline=blueprint_data.timeline)
        self.db.add(blueprint)
        await self.db.commit()
        await self.db.refresh(blueprint)
        return blueprint

    async def get_blueprint(self, token: str, blueprint_id: uuid.UUID) -> Optional[Blueprint]:
        user = await self._get_user_from_token(token)
        stmt = select(Blueprint).join(Idea).where(Blueprint.id == blueprint_id, Idea.user_id == user.id)
        result = await self.db.execute(stmt)
        blueprint = result.scalar_one_or_none()
        return blueprint

    async def _get_user_from_token(self, token: str) -> User:
        stmt = select(User).where(User.token == token)
        result = await self.db.execute(stmt)
        user = result.scalar_one()
        return user

    async def _get_idea(self, token: str, idea_id: uuid.UUID) -> Idea:
        user = await self._get_user_from_token(token)
        stmt = select(Idea).where(Idea.id == idea_id, Idea.user_id == user.id)
        result = await self.db.execute(stmt)
        idea = result.scalar_one()
        return idea
