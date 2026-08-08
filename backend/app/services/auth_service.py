import bcrypt
from backend.app.db.models import User
from backend.app.db.database import AsyncSessionLocal

class AuthService:
    async def authenticate(self, email: str, password: str):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                User.__table__.select().where(User.email == email)
            )
            user = result.scalar_one_or_none()
            if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                return user
        return None