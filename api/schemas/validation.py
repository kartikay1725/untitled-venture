from pydantic import BaseModel
from typing import Any

class ValidationResponse(BaseModel):
    validation_score: float
    validation_feedback: Any
    status: str
