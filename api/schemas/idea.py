from typing import List, Optional
from pydantic import BaseModel, Field, constr

class IdeaCreateRequest(BaseModel):
    description: constr(min_length=1, max_length=5000)
    industry_tags: List[constr(min_length=1, max_length=50)]

class IdeaResponse(BaseModel):
    ideaId: str
    validationScore: Optional[float]
    validationText: Optional[str]
    recommendedFeatures: List[str]

    class Config:
        orm_mode = True