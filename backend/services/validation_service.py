from sqlalchemy.ext.asyncio import AsyncSession
from ..engine.ai.validator import validate_idea
from ..database import Base
from uuid import uuid4

class ValidationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def validate_idea(self, idea_id: str):
        # Simulate async AI validation
        result = await validate_idea(idea_id)
        stmt = "UPDATE ideas SET validation_score = :score, validation_feedback = :feedback, status = 'validated' WHERE id = :id"
        await self.db.execute(stmt, {"id": idea_id, "score": result["score"], "feedback": result["feedback"]})
        await self.db.commit()
