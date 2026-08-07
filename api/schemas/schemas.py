from pydantic import BaseModel, EmailStr, Field, constr
from typing import List, Optional
import uuid

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr

    class Config:
        orm_mode = True

class IdeaCreate(BaseModel):
    description: str
    industry_tags: List[str]

class IdeaOut(BaseModel):
    id: uuid.UUID
    description: str
    industry_tags: List[str]
    validation_score: Optional[float]
    validation_text: Optional[str]

    class Config:
        orm_mode = True

class ValidationResult(BaseModel):
    validation_score: float
    validation_text: str
    recommended_features: List[str]

class MVPCreate(BaseModel):
    idea_id: uuid.UUID
    features: List[str]

class MVPOut(BaseModel):
    id: uuid.UUID
    status: str
    generated_code: Optional[str]

class DeploymentCreate(BaseModel):
    mvp_id: uuid.UUID
    target: str

class DeploymentOut(BaseModel):
    id: uuid.UUID
    status: str
    url: Optional[str]