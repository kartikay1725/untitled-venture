from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import RegisterRequest, LoginRequest, TokenResponse
from .models import User
from .security import get_password_hash, verify_password, create_access_token, create_refresh_token, get_user_by_email, get_user_by_id, decode_token
from .database import get_session
from sqlmodel import select, Session
import logging

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    async with get_session() as session:
        existing = await session.exec(select(User).where(User.email == request.email))
        if existing.first():
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(email=request.email, password_hash=get_password_hash(request.password))
        session.add(user)
        await session.commit()
        await session.refresh(user)
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    logger.info(f"User registered: {user.email}")
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    logger.info(f"User logged in: {user.email}")
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    token = auth_header.split(" ")[1]
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload["sub"]
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})
    logger.info(f"Refresh token rotated for user: {user.email}")
    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
