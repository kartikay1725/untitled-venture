from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime

class AuthRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    token: str
    user: dict

class IdeaCreate(BaseModel):
    description: str = Field(..., min_length=10)

class IdeaResponse(BaseModel):
    idea_id: UUID
    validation_score: Optional[float]
    validated_at: Optional[datetime]

class IdeaValidationResponse(BaseModel):
    validation_score: float
    validated_at: datetime

class MVPGenerateRequest(BaseModel):
    idea_id: UUID

class MVPGenerateResponse(BaseModel):
    mvp_id: UUID
    pdf_url: str
    download_url: str