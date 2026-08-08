from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    ideas = relationship("Idea", back_populates="user", cascade="all, delete-orphan")

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=False)
    validation_score = Column(Float)
    validated_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="ideas")
    blueprint = relationship("MVPBlueprint", uselist=False, back_populates="idea", cascade="all, delete-orphan")

class MVPBlueprint(Base):
    __tablename__ = "mvp_blueprints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False, unique=True)
    wireframes = Column(JSON, nullable=False)
    feature_list = Column(JSON, nullable=False)
    tech_stack = Column(JSON, nullable=False)
    timeline = Column(JSON, nullable=False)
    pdf_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    idea = relationship("Idea", back_populates="blueprint")
    package = relationship("MVPPackage", uselist=False, back_populates="blueprint", cascade="all, delete-orphan")

class MVPPackage(Base):
    __tablename__ = "mvp_packages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mvp_id = Column(UUID(as_uuid=True), ForeignKey("mvp_blueprints.id", ondelete="CASCADE"), nullable=False, unique=True)
    zip_url = Column(String(255), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    blueprint = relationship("MVPBlueprint", back_populates="package")