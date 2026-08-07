import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import UserRepository, IdeaRepository, IdempotencyRepository
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.domain.models import User, Idea
from datetime import datetime

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, email: str, password: str) -> Dict[str, Any]:
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        hashed = hash_password(password)
        user = await self.user_repo.create(email, hashed)
        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})
        return {"user_id": str(user.id), "access_token": access, "refresh_token": refresh}

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})
        return {"user_id": str(user.id), "access_token": access, "refresh_token": refresh}

    async def refresh(self, token: str) -> Dict[str, Any]:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")
        access = create_access_token({"sub": user_id})
        new_refresh = create_refresh_token({"sub": user_id})
        return {"access_token": access, "refresh_token": new_refresh}

class IdeaService:
    def __init__(self, db: AsyncSession):
        self.idea_repo = IdeaRepository(db)
        self.idemp_repo = IdempotencyRepository(db)

    async def create_idea(self, user_id: uuid.UUID, description: str, tags: List[str], idempotency_key: str) -> Dict[str, Any]:
        existing_key = await self.idemp_repo.get(idempotency_key)
        if existing_key:
            if existing_key.status == "completed":
                return existing_key.result
            else:
                raise ValueError("Duplicate idempotency key in use")
        await self.idemp_repo.create(idempotency_key, user_id, "create_idea")
        idea = await self.idea_repo.create(user_id, description, tags)
        # Simulated validation
        score = 0.75
        text = "Good potential"
        await self.idea_repo.update_validation(idea.id, score, text)
        result = {
            "idea_id": str(idea.id),
            "validation_score": float(score),
            "validation_text": text,
            "recommended_features": ["Feature A", "Feature B", "Feature C"],
        }
        await self.idemp_repo.set_result(idempotency_key, "completed", result)
        return result

    async def get_validation(self, idea_id: uuid.UUID) -> Dict[str, Any]:
        idea = await self.idea_repo.get(idea_id)
        if not idea or idea.validation_score is None:
            raise ValueError("Validation not found")
        return {
            "validation_score": float(idea.validation_score),
            "validation_text": idea.validation_text,
            "recommended_features": ["Feature A", "Feature B", "Feature C"],
        }
