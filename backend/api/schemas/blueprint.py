from pydantic import BaseModel
from typing import List, Dict

class BlueprintCreate(BaseModel):
    idea_id: str
    scope: str

class Feature(BaseModel):
    name: str
    description: str
    priority: int

class BlueprintOut(BaseModel):
    id: str
    features: List[Feature]
    timeline: Dict[str, str]
    class Config:
        orm_mode = True
