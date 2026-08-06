import asyncio
from ..database.engine import get_session
from ..api.models import Idea
from ..api.schemas import ValidationResponse
from fastapi import HTTPException
from sqlalchemy import select

class ValidationService:
    @staticmethod
    async def get_validation(idea_id: uuid.UUID) -> ValidationResponse:
        async with get_session() as session:
            result = await session.execute(select(Idea).where(Idea.id == idea_id))
            idea = result.scalars().first()
            if not idea:
                raise HTTPException(status_code=404, detail="Idea not found")
            if idea.validation_score is None:
                await asyncio.sleep(1)
                score = 0.75
                feedback = {"feasibility": "High", "risks": ["Market uncertainty"]}
                idea.validation_score = score
                idea.validation_feedback = feedback
                idea.status = "validated"
                session.add(idea)
                await session.commit()
            return ValidationResponse(validation_score=idea.validation_score, validation_feedback=idea.validation_feedback, status=idea.status)
