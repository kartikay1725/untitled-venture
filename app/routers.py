from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import uuid
from app.schemas import (
    AuthRegisterRequest,
    AuthRegisterResponse,
    AuthLoginRequest,
    AuthLoginResponse,
    IdeaCreateRequest,
    IdeaCreateResponse,
    IdeaValidationResponse,
)
from app.domain.services import AuthService, IdeaService
from app.utils.rate_limit import limiter
from app.utils.logging import log
from app.config import settings
from app.main import get_db_session
from app.utils.security import decode_token

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])
ideas_router = APIRouter(prefix="/api/ideas", tags=["ideas"])
health_router = APIRouter(prefix="/api", tags=["health"])

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db=Depends(get_db_session),
):
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = uuid.UUID(payload.get("sub"))
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@auth_router.post("/register", response_model=AuthRegisterResponse)
@limiter.limit(settings.RATE_LIMIT)
async def register(req: AuthRegisterRequest, db=Depends(get_db_session)):
    service = AuthService(db)
    try:
        res = await service.register(req.email, req.password)
        return AuthRegisterResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/login", response_model=AuthLoginResponse)
@limiter.limit(settings.RATE_LIMIT)
async def login(req: AuthLoginRequest, db=Depends(get_db_session)):
    service = AuthService(db)
    try:
        res = await service.login(req.email, req.password)
        return AuthLoginResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@auth_router.post("/refresh", response_model=AuthLoginResponse)
@limiter.limit(settings.RATE_LIMIT)
async def refresh(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db=Depends(get_db_session)):
    token = credentials.credentials
    service = AuthService(db)
    try:
        res = await service.refresh(token)
        return AuthLoginResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@ideas_router.post("/", response_model=IdeaCreateResponse)
@limiter.limit(settings.RATE_LIMIT)
async def create_idea(
    req: IdeaCreateRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db=Depends(get_db_session),
    user_id: uuid.UUID = Depends(get_current_user),
):
    service = IdeaService(db)
    try:
        res = await service.create_idea(user_id, req.description, req.industry_tags, idempotency_key)
        return IdeaCreateResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@ideas_router.get("/{idea_id}/validation", response_model=IdeaValidationResponse)
@limiter.limit(settings.RATE_LIMIT)
async def get_validation(
    idea_id: uuid.UUID,
    db=Depends(get_db_session),
):
    service = IdeaService(db)
    try:
        res = await service.get_validation(idea_id)
        return IdeaValidationResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@health_router.get("/health")
async def health():
    return JSONResponse(content={"status": "ok", "db": "ok"})
