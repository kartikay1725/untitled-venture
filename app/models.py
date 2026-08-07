import uuid
from sqlalchemy import Column, String, Text, DateTime, Numeric, JSON, ARRAY, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    industry_tags = Column(ARRAY(String), nullable=False)
    validation_score = Column(Numeric, nullable=True)
    validation_text = Column(Text, nullable=True)
    recommended_features = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MVPTemplate(Base):
    __tablename__ = "mvp_templates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    features = Column(JSON, nullable=False)
    generated_code = Column(Text, nullable=True)
    status = Column(Enum("pending","ready","failed", name="mvp_status"), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Deployment(Base):
    __tablename__ = "deployments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mvp_id = Column(UUID(as_uuid=True), ForeignKey("mvp_templates.id"), nullable=False)
    target = Column(String(255), nullable=False)
    url = Column(String(255), nullable=True)
    status = Column(Enum("queued","deploying","success","error", name="deploy_status"), nullable=False, default="queued")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
