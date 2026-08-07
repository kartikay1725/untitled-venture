from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import List, Optional

@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    role: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Idea:
    id: UUID
    user_id: UUID
    description: str
    industry_tags: List[str]
    validation_score: Optional[float]
    validation_text: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class IdempotencyKey:
    key: str
    user_id: UUID
    operation: str
    status: str
    result: Optional[dict]
