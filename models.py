import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from passlib.context import CryptContext
import jwt

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    token = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)

    def generate_token(self) -> str:
        payload = {"sub": str(self.id), "email": self.email}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        self.token = token
        return token

class Idea(Base):
    __tablename__ = "ideas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    validation_score = Column(Numeric, nullable=True)
    validation_feedback = Column(JSON, nullable=True)
    status = Column(String(50), default="pending")
    user = relationship("User", backref="ideas")

class Blueprint(Base):
    __tablename__ = "mvp_blueprints"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id"), nullable=False)
    features = Column(JSON, nullable=False)
    timeline = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    idea = relationship("Idea", backref="blueprints")
