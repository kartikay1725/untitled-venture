from pydantic import BaseModel, Field
from uuid import UUID

class IdeaCreate(BaseModel):
    title: str = Field(..., min_length=5)
    description: str = Field(..., min_length=20)

class IdeaResponse(BaseModel):
    id: UUID
    title: str
    description: str
    submitted_at: str
    status: str
