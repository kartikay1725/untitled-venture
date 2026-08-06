from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Idea
from uuid import UUID

class IdeaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, title: str, description: str) -> Idea:
        idea = Idea(user_id=user_id, title=title, description=description)
        self.session.add(idea)
        await self.session.commit()
        await self.session.refresh(idea)
        return idea

    async def get(self, idea_id: UUID) -> Idea | None:
        result = await self.session.execute(select(Idea).where(Idea.id == idea_id))
        return result.scalar_one_or_none()

    async def update_validation(self, idea: Idea, score: float, feedback: dict):
        idea.validation_score = score
        idea.validation_feedback = feedback
        idea.status = "validated"
        await self.session.commit()
