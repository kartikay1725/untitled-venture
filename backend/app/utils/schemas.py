from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserOut(BaseModel):
    id: str
    email: EmailStr

class Token(BaseModel):
    token: str
    user: UserOut

class IdeaCreate(BaseModel):
    description: str

class IdeaOut(BaseModel):
    id: str
    validation_score: Optional[float]
    validated_at: Optional[datetime]

class ValidationResult(BaseModel):
    validation_score: float
    validated_at: datetime

class MVPBlueprintOut(BaseModel):
    mvp_id: str
    pdf_url: str
    download_url: str