import random
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.idea_repo import IdeaRepository

class ValidationService:
    def __init__(self, session: AsyncSession):
        self.repo = IdeaRepository(session)

    async def validate(self, idea_id: UUID):
        idea = await self.repo.get(idea_id)
        if not idea:
            raise ValueError("Idea not found")
        # Simple heuristic: longer description => higher score
        score = min(1.0, len(idea.description.split()) / 200)
        feedback = {"length": len(idea.description.split()), "score": score}
        await self.repo.update_validation(idea, score, feedback)
        return score, feedback
