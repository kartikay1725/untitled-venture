import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.utils.settings import Settings

settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire, "iss": settings.JWT_ISSUER, "aud": settings.JWT_AUDIENCE})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"], audience=settings.JWT_AUDIENCE, issuer=settings.JWT_ISSUER)

class verify_password:
    @staticmethod
    def hash(password: str) -> str:
        return pwd_context.hash(password)
    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)