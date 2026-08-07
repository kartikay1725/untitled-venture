from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ideas: List["Idea"] = Relationship(back_populates="user")

class Idea(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    description: str
    industry_tags: List[str] = Field(sa_column_kwargs={"type_": ARRAY(ARRAY)} )
    validation_score: Optional[float] = None
    validation_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user: Optional[User] = Relationship(back_populates="ideas")
    mvp_templates: List["MVPTemplate"] = Relationship(back_populates="idea")

class MVPTemplate(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    idea_id: uuid.UUID = Field(foreign_key="idea.id")
    features: List[str] = Field(sa_column_kwargs={"type_": JSONB})
    generated_code: Optional[str] = None
    status: str = Field(default="pending", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    idea: Optional[Idea] = Relationship(back_populates="mvp_templates")
    deployments: List["Deployment"] = Relationship(back_populates="mvp")

class Deployment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    mvp_id: uuid.UUID = Field(foreign_key="mvptemplate.id")
    target: str
    url: Optional[str] = None
    status: str = Field(default="queued", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    mvp: Optional[MVPTemplate] = Relationship(back_populates="deployments")