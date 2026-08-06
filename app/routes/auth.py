from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from uuid import UUID
from app.services.user_service import UserService
from app.schemas import AuthRegister, Token
from app.config import settings
from app.database import get_session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return UUID(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register", response_model=Token)
async def register(data: AuthRegister, session=Depends(get_session)):
    service = UserService(session)
    try:
        user_id = await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token = jwt.encode({"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return Token(access_token=token)

@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    service = UserService(session)
    try:
        user_id = await service.authenticate(form.username, form.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token = jwt.encode({"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return Token(access_token=token)
