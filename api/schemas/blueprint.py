from pydantic import BaseModel
from typing import List, Dict, Any
from uuid import UUID

class BlueprintCreate(BaseModel):
    idea_id: UUID
    scope: str

class BlueprintResponse(BaseModel):
    id: UUID
    features: List[Dict[str, Any]]
    timeline: Dict[str, Any]
