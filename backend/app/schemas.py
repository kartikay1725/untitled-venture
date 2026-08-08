from pydantic import BaseModel, EmailStr
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    user: dict

class IdeaCreateRequest(BaseModel):
    description: str

class IdeaValidationResponse(BaseModel):
    idea_id: str
    validation_score: float
    validated_at: datetime

class MVPGenerateRequest(BaseModel):
    idea_id: str

class MVPGenerateResponse(BaseModel):
    mvp_id: str
    pdf_url: str
    download_url: str