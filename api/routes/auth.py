from fastapi import APIRouter, Depends, HTTPException, status
from api.schemas import UserCreate, Token
from api.services.auth_service import AuthService
from api.utils.auth import get_current_user, create_access_token
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.register(user_in)
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    token = await service.login(user_in.email, user_in.password)
    return {"access_token": token, "token_type": "bearer"}