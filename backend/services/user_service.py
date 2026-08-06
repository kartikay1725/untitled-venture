from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import Base, engine
from ..api.schemas.auth import UserCreate, UserOut
from passlib.context import CryptContext
from uuid import uuid4
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_in: UserCreate) -> UserOut:
        hashed = pwd_context.hash(user_in.password)
        stmt = select(Base.metadata.tables["users"]).where(Base.metadata.tables["users"].c.email == user_in.email)
        result = await self.db.execute(stmt)
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")
        user = {
            "id": str(uuid4()),
            "email": user_in.email,
            "password_hash": hashed,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        await self.db.execute("INSERT INTO users (id, email, password_hash, created_at, updated_at) VALUES (:id, :email, :password_hash, :created_at, :updated_at)", user)
        await self.db.commit()
        return UserOut(**user)

    async def authenticate(self, email: str, password: str):
        stmt = select(Base.metadata.tables["users"]).where(Base.metadata.tables["users"].c.email == email)
        result = await self.db.execute(stmt)
        user = result.fetchone()
        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user
