import uuid
from ..database.engine import get_session
from ..api.models import MVPBlueprint
from ..api.schemas import BlueprintCreateRequest, BlueprintResponse, Feature, Timeline
from fastapi import HTTPException
from sqlalchemy import select

class BlueprintService:
    @staticmethod
    async def generate_blueprint(idea_id: uuid.UUID, scope: str) -> BlueprintResponse:
        async with get_session() as session:
            result = await session.execute(select(MVPBlueprint).where(MVPBlueprint.idea_id == idea_id))
            existing = result.scalars().first()
            if existing:
                raise HTTPException(status_code=400, detail="Blueprint already exists")
            features = [
                {"name": "Login", "description": "User authentication", "priority": 1},
                {"name": "Idea Submission", "description": "Submit ideas", "priority": 2},
                {"name": "Validation", "description": "AI validation", "priority": 3}
            ]
            timeline = {"start_date": "2024-09-01", "end_date": "2024-09-30", "milestones": ["Design", "Development", "Testing"]}
            blueprint = MVPBlueprint(id=uuid.uuid4(), idea_id=idea_id, features=features, timeline=timeline)
            session.add(blueprint)
            await session.commit()
            await session.refresh(blueprint)
            return BlueprintResponse(features=features, timeline=timeline)

    @staticmethod
    async def get_blueprint(blueprint_id: uuid.UUID) -> BlueprintResponse:
        async with get_session() as session:
            result = await session.execute(select(MVPBlueprint).where(MVPBlueprint.id == blueprint_id))
            blueprint = result.scalars().first()
            if not blueprint:
                raise HTTPException(status_code=404, detail="Blueprint not found")
            return BlueprintResponse(features=blueprint.features, timeline=blueprint.timeline)
