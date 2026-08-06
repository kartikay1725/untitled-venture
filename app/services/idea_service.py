from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.idea_repo import IdeaRepository
from app.schemas import IdeaCreate

class IdeaService:
    def __init__(self, session: AsyncSession):
        self.repo = IdeaRepository(session)

    async def submit(self, user_id: UUID, data: IdeaCreate) -> UUID:
        idea = await self.repo.create(user_id, data.title, data.description)
        return idea.id

    async def get(self, idea_id: UUID):
        return await self.repo.get(idea_id)
