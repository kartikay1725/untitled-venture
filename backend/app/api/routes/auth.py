from fastapi import APIRouter, Depends, HTTPException, status
from ...services.user_service import UserService
from ...api.schemas import RegisterRequest, LoginRequest, TokenResponse
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest):
    return await UserService.register(req.email, req.password)

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    return await UserService.authenticate(req.email, req.password)
