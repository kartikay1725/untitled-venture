import uuid
from sqlalchemy import Column, String, Text, ARRAY, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .db import Base
from datetime import datetime

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    description = Column(Text, nullable=False)
    industry_tags = Column(ARRAY(String), nullable=False)
    validation_score = Column(Numeric, nullable=True)
    validation_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)