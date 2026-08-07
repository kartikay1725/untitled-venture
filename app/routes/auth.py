from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import async_session
from app.schemas import UserCreate, Token
from app.models import User
from app.utils.security import get_password_hash, create_access_token, verify_password
import uuid
import logging

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_in: UserCreate):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == user_in.email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(
            id=uuid.uuid4(),
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password)
        )
        session.add(user)
        await session.commit()
        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type":"bearer"}

@router.post("/login", response_model=Token)
async def login(user_in: UserCreate):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == user_in.email))
        user = result.scalars().first()
        if not user or not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type":"bearer"}
