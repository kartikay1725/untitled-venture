import uuid
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ARRAY, JSONB
from sqlalchemy import String, Text, Numeric, TIMESTAMP, CheckConstraint
from datetime import datetime
from app.domain.models import User, Idea, IdempotencyKey

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="user")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default="now()")
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default="now()", onupdate=datetime.utcnow)

class IdeaModel(Base):
    __tablename__ = "ideas"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    industry_tags: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    validation_score: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    validation_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default="now()")
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default="now()", onupdate=datetime.utcnow)

class IdempotencyKeyModel(Base):
    __tablename__ = "idempotency_keys"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    operation: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default="now()")
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default="now()", onupdate=datetime.utcnow)

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        user_model = result.scalar_one_or_none()
        if user_model:
            return User(
                id=user_model.id,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                role=user_model.role,
                created_at=user_model.created_at,
                updated_at=user_model.updated_at,
            )
        return None

    async def create(self, email: str, hashed_password: str) -> User:
        user_model = UserModel(email=email, hashed_password=hashed_password)
        self.db.add(user_model)
        await self.db.flush()
        return User(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            role=user_model.role,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

class IdeaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: uuid.UUID, description: str, tags: List[str]) -> Idea:
        idea_model = IdeaModel(user_id=user_id, description=description, industry_tags=tags)
        self.db.add(idea_model)
        await self.db.flush()
        return Idea(
            id=idea_model.id,
            user_id=idea_model.user_id,
            description=idea_model.description,
            industry_tags=idea_model.industry_tags,
            validation_score=idea_model.validation_score,
            validation_text=idea_model.validation_text,
            created_at=idea_model.created_at,
            updated_at=idea_model.updated_at,
        )

    async def get(self, idea_id: uuid.UUID) -> Optional[Idea]:
        result = await self.db.execute(select(IdeaModel).where(IdeaModel.id == idea_id))
        idea_model = result.scalar_one_or_none()
        if idea_model:
            return Idea(
                id=idea_model.id,
                user_id=idea_model.user_id,
                description=idea_model.description,
                industry_tags=idea_model.industry_tags,
                validation_score=idea_model.validation_score,
                validation_text=idea_model.validation_text,
                created_at=idea_model.created_at,
                updated_at=idea_model.updated_at,
            )
        return None

    async def update_validation(self, idea_id: uuid.UUID, score: float, text: str) -> None:
        await self.db.execute(
            update(IdeaModel)
            .where(IdeaModel.id == idea_id)
            .values(validation_score=score, validation_text=text, updated_at=datetime.utcnow())
        )
        await self.db.flush()

class IdempotencyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, key: str) -> Optional[IdempotencyKey]:
        result = await self.db.execute(select(IdempotencyKeyModel).where(IdempotencyKeyModel.key == key))
        model = result.scalar_one_or_none()
        if model:
            return IdempotencyKey(
                key=model.key,
                user_id=model.user_id,
                operation=model.operation,
                status=model.status,
                result=model.result,
            )
        return None

    async def create(self, key: str, user_id: uuid.UUID, operation: str) -> IdempotencyKey:
        model = IdempotencyKeyModel(key=key, user_id=user_id, operation=operation, status="pending")
        self.db.add(model)
        await self.db.flush()
        return IdempotencyKey(
            key=model.key,
            user_id=model.user_id,
            operation=model.operation,
            status=model.status,
            result=model.result,
        )

    async def set_result(self, key: str, status: str, result: dict) -> None:
        await self.db.execute(
            update(IdempotencyKeyModel)
            .where(IdempotencyKeyModel.key == key)
            .values(status=status, result=result, updated_at=datetime.utcnow())
        )
        await self.db.flush()
