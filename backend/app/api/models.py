from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, UUID, TIMESTAMP, Text, Numeric, JSON, ForeignKey, func
import uuid
from sqlalchemy.dialects.postgresql import UUID as PGUUID

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    submitted_at = Column(TIMESTAMP, default=func.now())
    validation_score = Column(Numeric)
    validation_feedback = Column(JSON)
    status = Column(String(50), default="pending")

class MVPBlueprint(Base):
    __tablename__ = "mvp_blueprints"
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(PGUUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    features = Column(JSON, nullable=False)
    timeline = Column(JSON)
    created_at = Column(TIMESTAMP, default=func.now())
