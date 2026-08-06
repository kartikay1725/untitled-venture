from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user_repo import UserRepository
from app.schemas import AuthRegister
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def register(self, data: AuthRegister) -> UUID:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")
        hashed = pwd_context.hash(data.password)
        user = await self.repo.create(data.email, hashed)
        return user.id

    async def authenticate(self, email: str, password: str) -> UUID:
        user = await self.repo.get_by_email(email)
        if not user or not pwd_context.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return user.id
