import uuid
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import select
from ..database.engine import get_session
from ..api.models import User
from ..api.schemas import TokenResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserService:
    @staticmethod
    async def register(email: str, password: str) -> TokenResponse:
        async with get_session() as session:
            existing = await session.execute(select(User).where(User.email == email))
            if existing.scalars().first():
                raise HTTPException(status_code=400, detail="Email already registered")
            user = User(id=uuid.uuid4(), email=email, password_hash=pwd_context.hash(password))
            session.add(user)
            await session.commit()
            return UserService.create_token(user.id)

    @staticmethod
    async def authenticate(email: str, password: str) -> TokenResponse:
        async with get_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user or not pwd_context.verify(password, user.password_hash):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return UserService.create_token(user.id)

    @staticmethod
    def create_token(user_id: uuid.UUID) -> TokenResponse:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": str(user_id), "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return TokenResponse(access_token=encoded_jwt, token_type="bearer")

    @staticmethod
    def get_user_id_from_token(token: str) -> uuid.UUID:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return uuid.UUID(payload.get("sub"))
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
