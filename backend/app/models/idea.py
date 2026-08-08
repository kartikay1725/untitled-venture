from ..db.database import Base
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    validation_score = Column(Float)
    validated_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)