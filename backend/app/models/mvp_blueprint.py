from ..db.database import Base
from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class MVPBlueprint(Base):
    __tablename__ = "mvp_blueprints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    wireframes = Column(JSON, nullable=False)
    feature_list = Column(JSON, nullable=False)
    tech_stack = Column(JSON, nullable=False)
    timeline = Column(JSON, nullable=False)
    pdf_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)