import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.engine import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()", onupdate="now()")

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    submitted_at = Column(TIMESTAMP, server_default="now()")
    validation_score = Column(Numeric)
    validation_feedback = Column(JSON)
    status = Column(String(50), default="pending")

class MVPBlueprint(Base):
    __tablename__ = "mvp_blueprints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    features = Column(JSON, nullable=False)
    timeline = Column(JSON)
    created_at = Column(TIMESTAMP, server_default="now()")
