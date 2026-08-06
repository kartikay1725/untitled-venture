from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Idea, IdeaStatus
from .schemas import IdeaCreate, IdeaResponse
import uuid

async def create_idea(session: AsyncSession, user_id: uuid.UUID, idea_in: IdeaCreate) -> Idea:
    idea = Idea(user_id=user_id, title=idea_in.title, description=idea_in.description)
    session.add(idea)
    await session.commit()
    await session.refresh(idea)
    return idea

async def get_idea_validation(session: AsyncSession, idea_id: uuid.UUID) -> Idea:
    result = await session.execute(select(Idea).where(Idea.id == idea_id))
    idea = result.scalar_one_or_none()
    return idea
