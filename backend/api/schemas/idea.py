from pydantic import BaseModel, Field
from typing import Optional

class IdeaCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str

class IdeaOut(BaseModel):
    id: str
    title: str
    description: str
    validation_score: Optional[float]
    validation_feedback: Optional[dict]
    status: str
    class Config:
        orm_mode = True
