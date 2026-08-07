import hashlib
import hmac
import os
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Tuple, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User, Idea, MvpTemplate, Deployment
from .schemas import UserCreate

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

class AuthService:
    def hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"{salt}${pwd_hash}"

    def verify_password(self, plain: str, hashed: str) -> bool:
        salt, pwd_hash = hashed.split("$")
        return hmac.compare_digest(pwd_hash, hashlib.sha256((salt + plain).encode()).hexdigest())

    async def register(self, user_in: UserCreate, db: AsyncSession) -> User:
        stmt = select(User).where(User.email == user_in.email)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")
        user = User(email=user_in.email, hashed_password=self.hash_password(user_in.password))
        db.add(user)
        await db.flush()
        return user

    async def authenticate(self, email: str, password: str, db: AsyncSession) -> User:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user or not self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        return user

    def create_token(self, user_id: UUID) -> str:
        payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)}
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def get_user_id_from_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return UUID(payload["sub"])
        except Exception as e:
            raise ValueError("Invalid token") from e

class IdeaService:
    async def create_idea(self, user_id: UUID, idea_in, db: AsyncSession) -> Idea:
        idea = Idea(user_id=user_id, description=idea_in.description, industry_tags=idea_in.industry_tags)
        db.add(idea)
        await db.flush()
        return idea

    async def get_idea(self, idea_id: str, db: AsyncSession) -> Idea:
        stmt = select(Idea).where(Idea.id == idea_id)
        result = await db.execute(stmt)
        idea = result.scalar_one_or_none()
        if not idea:
            raise ValueError("Idea not found")
        return idea

class ValidationService:
    def __init__(self, ai_stub):
        self.ai = ai_stub

    async def validate(self, description: str, tags: List[str], db: AsyncSession) -> Tuple[float, str, List[str]]:
        # Simulated async AI call
        score, text, features = self.ai.generate_validation(description, tags)
        return score, text, features

class MvpService:
    async def create_mvp(self, idea_id: str, features: List[str], db: AsyncSession) -> MvpTemplate:
        mvp = MvpTemplate(idea_id=idea_id, features=features)
        db.add(mvp)
        await db.flush()
        return mvp

    async def get_mvp(self, mvp_id: str, db: AsyncSession) -> MvpTemplate:
        stmt = select(MvpTemplate).where(MvpTemplate.id == mvp_id)
        result = await db.execute(stmt)
        mvp = result.scalar_one_or_none()
        if not mvp:
            raise ValueError("MVP not found")
        return mvp

class DeploymentService:
    async def deploy(self, mvp_id: str, target: str, db: AsyncSession) -> Deployment:
        deployment = Deployment(mvp_id=mvp_id, target=target)
        db.add(deployment)
        await db.flush()
        # Simulate deployment success
        deployment.status = "success"
        deployment.url = f"https://{target}.example.com/{mvp_id}"
        await db.flush()
        return deployment

    async def get_deployment(self, deployment_id: str, db: AsyncSession) -> Deployment:
        stmt = select(Deployment).where(Deployment.id == deployment_id)
        result = await db.execute(stmt)
        dep = result.scalar_one_or_none()
        if not dep:
            raise ValueError("Deployment not found")
        return dep
