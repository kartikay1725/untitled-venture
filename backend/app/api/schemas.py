from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from uuid import UUID

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class IdeaCreateRequest(BaseModel):
    title: str
    description: str

class IdeaResponse(BaseModel):
    id: UUID
    title: str
    description: str
    submitted_at: str
    status: str

class ValidationResponse(BaseModel):
    validation_score: Optional[float]
    validation_feedback: Optional[dict]
    status: str

class BlueprintCreateRequest(BaseModel):
    idea_id: UUID
    scope: str

class Feature(BaseModel):
    name: str
    description: str
    priority: int

class Timeline(BaseModel):
    start_date: str
    end_date: str
    milestones: List[str]

class BlueprintResponse(BaseModel):
    features: List[Feature]
    timeline: Timeline
