from sqlalchemy.ext.asyncio import AsyncSession
from .models import MVPBlueprint, Idea
from .schemas import BlueprintCreate, BlueprintResponse
import uuid
import random

async def generate_blueprint(session: AsyncSession, blueprint_in: BlueprintCreate) -> MVPBlueprint:
    # Simulate AI processing with deterministic data
    features = [
        {"name": f"Feature {i+1}", "description": f"Description for feature {i+1}"}
        for i in range(random.randint(3, 7))
    ]
    timeline = {"start_date": "2024-09-01", "end_date": "2024-12-01"}
    blueprint = MVPBlueprint(idea_id=blueprint_in.idea_id, features=features, timeline=timeline)
    session.add(blueprint)
    await session.commit()
    await session.refresh(blueprint)
    return blueprint
