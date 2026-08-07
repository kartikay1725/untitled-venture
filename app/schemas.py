from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[UUID] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserOut(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        orm_mode = True

class IdeaCreate(BaseModel):
    description: str
    industry_tags: List[str]

class IdeaOut(BaseModel):
    id: UUID
    description: str
    industry_tags: List[str]
    validation_score: Optional[float]
    validation_text: Optional[str]
    recommended_features: Optional[List[str]]

    class Config:
        orm_mode = True

class ValidationResult(BaseModel):
    validationScore: float
    validationText: str
    recommendedFeatures: List[str]

class MVPCreate(BaseModel):
    ideaId: UUID
    features: List[str]

class MVPOut(BaseModel):
    mvpId: UUID
    status: str
    generatedCode: Optional[str] = None

class DeploymentCreate(BaseModel):
    mvpId: UUID
    target: str

class DeploymentOut(BaseModel):
    deploymentId: UUID
    status: str
    url: Optional[str] = None
