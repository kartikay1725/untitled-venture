from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Blueprint
from uuid import UUID

class BlueprintRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, idea_id: UUID, features: list, timeline: list) -> Blueprint:
        blueprint = Blueprint(idea_id=idea_id, features=features, timeline=timeline)
        self.session.add(blueprint)
        await self.session.commit()
        await self.session.refresh(blueprint)
        return blueprint

    async def get(self, blueprint_id: UUID) -> Blueprint | None:
        result = await self.session.execute(select(Blueprint).where(Blueprint.id == blueprint_id))
        return result.scalar_one_or_none()
