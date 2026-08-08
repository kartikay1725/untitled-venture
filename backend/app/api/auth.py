from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr, BaseModel
import uuid
from ..db import get_db
from ..models import User
from ..utils.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr

class TokenResponse(BaseModel):
    token: str
    user: UserResponse

@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(id=uuid.uuid4(), email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(token=token, user=UserResponse(id=user.id, email=user.email))

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(token=token, user=UserResponse(id=user.id, email=user.email))