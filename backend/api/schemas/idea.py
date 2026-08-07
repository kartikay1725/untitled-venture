from pydantic import BaseModel, Field
from typing import List

class IdeaCreate(BaseModel):
    user_id: str
    description: str
    industry_tags: List[str] = Field(default_factory=list)

class IdeaResponse(BaseModel):
    idea_id: str
    validation_score: float
    validation_text: str
    recommended_features: List[str]