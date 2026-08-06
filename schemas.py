from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class IdeaCreate(BaseModel):
    title: str
    description: str

class IdeaResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    submitted_at: datetime
    validation_score: Optional[float]
    validation_feedback: Optional[Dict]
    status: str

    class Config:
        orm_mode = True

class ValidationResponse(BaseModel):
    validation_score: Optional[float]
    validation_feedback: Optional[Dict]
    status: str

class BlueprintCreate(BaseModel):
    idea_id: uuid.UUID
    scope: str

class BlueprintResponse(BaseModel):
    id: uuid.UUID
    features: List[Dict]
    timeline: Optional[Dict]
    created_at: datetime

    class Config:
        orm_mode = True
