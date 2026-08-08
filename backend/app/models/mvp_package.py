from ..db.database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class MVPPackage(Base):
    __tablename__ = "mvp_packages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mvp_id = Column(UUID(as_uuid=True), ForeignKey("mvp_blueprints.id"), nullable=False)
    zip_url = Column(String(255), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)