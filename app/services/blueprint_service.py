from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.blueprint_repo import BlueprintRepository

class BlueprintService:
    def __init__(self, session: AsyncSession):
        self.repo = BlueprintRepository(session)

    async def generate(self, idea_id: UUID, scope: str):
        # Dummy feature list based on scope
        features = [
            {"name": "Login", "description": "User authentication", "priority": 1},
            {"name": "Dashboard", "description": "Overview of metrics", "priority": 2},
            {"name": "Export", "description": f"Export to {scope}", "priority": 3},
        ]
        timeline = [
            {"sprint": 1, "duration_days": 14},
            {"sprint": 2, "duration_days": 14},
        ]
        blueprint = await self.repo.create(idea_id, features, timeline)
        return blueprint.id
