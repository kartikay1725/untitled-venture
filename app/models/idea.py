from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, Text, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    validation_score = Column(Float)
    validated_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)