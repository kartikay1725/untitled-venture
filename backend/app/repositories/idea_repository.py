from sqlalchemy.orm import Session
from .models.idea import Idea
from uuid import UUID
from datetime import datetime

class IdeaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: UUID, description: str) -> Idea:
        idea = Idea(user_id=user_id, description=description)
        self.db.add(idea)
        self.db.commit()
        self.db.refresh(idea)
        return idea

    def get(self, idea_id: UUID) -> Idea | None:
        return self.db.query(Idea).filter(Idea.id == idea_id).first()

    def update_validation(self, idea: Idea, score: float) -> Idea:
        idea.validation_score = score
        idea.validated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(idea)
        return idea