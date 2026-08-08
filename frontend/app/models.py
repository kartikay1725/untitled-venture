"""SQLAlchemy models.

Using declarative base with UUID primary keys.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    description = Column(String, nullable=False)
    validation_score = Column(Float)
    validated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class MVPBlueprint(Base):
    __tablename__ = "mvp_blueprints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    wireframes = Column(JSON)
    feature_list = Column(JSON)
    tech_stack = Column(JSON)
    timeline = Column(JSON)
    pdf_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class MVPPackage(Base):
    __tablename__ = "mvp_packages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mvp_id = Column(UUID(as_uuid=True), ForeignKey("mvp_blueprints.id"), nullable=False)
    zip_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)