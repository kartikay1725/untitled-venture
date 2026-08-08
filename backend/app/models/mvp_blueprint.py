from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, JSON, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class MVPBlueprint(Base):
    __tablename__ = "mvp_blueprints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    wireframes = Column(JSON)
    feature_list = Column(JSON)
    tech_stack = Column(JSON)
    timeline = Column(JSON)
    pdf_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)