from sqlalchemy.ext.asyncio import AsyncSession
from ..database import Base
from ..api.schemas.idea import IdeaCreate, IdeaOut
from uuid import uuid4
from datetime import datetime

class IdeaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_idea(self, idea_in: IdeaCreate, user_id: str):
        idea = {
            "id": str(uuid4()),
            "user_id": user_id,
            "title": idea_in.title,
            "description": idea_in.description,
            "submitted_at": datetime.utcnow(),
            "status": "pending",
        }
        await self.db.execute("INSERT INTO ideas (id, user_id, title, description, submitted_at, status) VALUES (:id, :user_id, :title, :description, :submitted_at, :status)", idea)
        await self.db.commit()
        return IdeaOut(**idea)

    async def get_idea(self, idea_id: str, user_id: str):
        stmt = select(Base.metadata.tables["ideas"]).where(Base.metadata.tables["ideas"].c.id == idea_id, Base.metadata.tables["ideas"].c.user_id == user_id)
        result = await self.db.execute(stmt)
        row = result.fetchone()
        if not row:
            return None
        return IdeaOut(**row)
