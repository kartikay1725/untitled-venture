import uuid
import bcrypt
from backend.app.db.models import User
from backend.app.db.database import AsyncSessionLocal

class UserService:
    async def get_by_email(self, email: str):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                User.__table__.select().where(User.email == email)
            )
            return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                User.__table__.select().where(User.id == user_id)
            )
            return result.scalar_one_or_none()

    async def create_user(self, email: str, password: str):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(email=email, password_hash=hashed)
        async with AsyncSessionLocal() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user