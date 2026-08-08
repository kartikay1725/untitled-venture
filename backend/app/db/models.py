import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from backend.app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    validation_score = Column(Float)
    validated_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", backref="ideas")

class MVPBlueprint(Base):
    __tablename__ = "mvp_blueprints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    wireframes = Column(JSONB)
    feature_list = Column(JSONB)
    tech_stack = Column(JSONB)
    timeline = Column(JSONB)
    pdf_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class MVPPackage(Base):
    __tablename__ = "mvp_packages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mvp_id = Column(UUID(as_uuid=True), ForeignKey("mvp_blueprints.id"), nullable=False)
    zip_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)