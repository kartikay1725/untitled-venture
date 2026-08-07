from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Idea
from api.schemas import IdeaCreate, IdeaOut
from sqlalchemy import select
from datetime import datetime
import uuid
from fastapi import HTTPException

class IdeaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_idea(self, user_id: uuid.UUID, idea_in: IdeaCreate) -> IdeaOut:
        idea = Idea(
            id=uuid.uuid4(),
            user_id=user_id,
            description=idea_in.description,
            industry_tags=idea_in.industry_tags,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(idea)
        await self.db.commit()
        await self.db.refresh(idea)
        return IdeaOut.from_orm(idea)

    async def get_idea(self, idea_id: uuid.UUID) -> IdeaOut:
        result = await self.db.execute(select(Idea).where(Idea.id == idea_id))
        idea = result.scalar_one_or_none()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        return IdeaOut.from_orm(idea)