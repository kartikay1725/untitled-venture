from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, Dict, Any

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Idea(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    validation_score: Optional[float] = Field(default=None)
    validation_feedback: Optional[Dict[str, Any]] = Field(default=None)
    status: str = Field(default="pending")

class Blueprint(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    idea_id: UUID = Field(foreign_key="idea.id", nullable=False)
    features: Dict[str, Any] = Field(nullable=False)
    timeline: Dict[str, Any] = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
