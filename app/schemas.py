from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class IdeaRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)

    @validator("description")
    def sanitize_description(cls, v):
        import bleach
        return bleach.clean(v)

class IdeaResponse(BaseModel):
    id: UUID
    title: str
    description: str
    submitted_at: datetime
    validation_score: Optional[float]
    validation_feedback: Optional[Dict[str, Any]]
    status: str

class ValidationResponse(BaseModel):
    validation_score: Optional[float]
    validation_feedback: Optional[Dict[str, Any]]
    status: str

class BlueprintRequest(BaseModel):
    idea_id: UUID
    scope: str

class BlueprintResponse(BaseModel):
    id: UUID
    features: Dict[str, Any]
    timeline: Dict[str, Any]
    created_at: datetime
