from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from uuid import UUID
from .services.auth_service import AuthService
from .services.user_service import UserService
from .repositories.user_repository import UserRepository
from .database import SessionLocal
from .utils.idempotency import IdempotencyStore
from .utils.logger import logger
from .utils.limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])
limiter.limit("10/minute")(router)
idempotency_store = IdempotencyStore()

class RegisterDTO(BaseModel):
    email: EmailStr
    password: str

class LoginDTO(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    user: dict


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db=Depends(get_db)):
    return UserService(UserRepository(db))


def get_auth_service(user_service=Depends(get_user_service)):
    return AuthService(user_service.user_repo)

@router.post("/register", response_model=TokenResponse)
@limiter.limit("5/minute")
def register(dto: RegisterDTO, request: Request, auth_service: AuthService = Depends(get_auth_service)):
    idempotency_key = request.headers.get("Idempotency-Key")
    if idempotency_key:
        cached = id