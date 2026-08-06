from sqlalchemy.ext.asyncio import AsyncSession
from ..database import Base
from ..api.schemas.blueprint import BlueprintCreate, BlueprintOut
from uuid import uuid4
from datetime import datetime
from ..engine.ai.blueprint_generator import generate_blueprint

class BlueprintService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_blueprint(self, blueprint_in: BlueprintCreate, user_id: str):
        # Ensure idea exists and belongs to user
        stmt = "SELECT * FROM ideas WHERE id = :id AND user_id = :user_id"
        result = await self.db.execute(stmt, {"id": blueprint_in.idea_id, "user_id": user_id})
        if not result.fetchone():
            raise ValueError("Idea not found or access denied")
        # Generate blueprint via AI
        features, timeline = await generate_blueprint(blueprint_in.scope)
        blueprint = {
            "id": str(uuid4()),
            "idea_id": blueprint_in.idea_id,
            "features": features,
            "timeline": timeline,
            "created_at": datetime.utcnow(),
        }
        await self.db.execute("INSERT INTO mvp_blueprints (id, idea_id, features, timeline, created_at) VALUES (:id, :idea_id, :features, :timeline, :created_at)", blueprint)
        await self.db.commit()
        return BlueprintOut(**blueprint)

    async def get_blueprint(self, blueprint_id: str, user_id: str):
        stmt = "SELECT * FROM mvp_blueprints WHERE id = :id"
        result = await self.db.execute(stmt, {"id": blueprint_id})
        row = result.fetchone()
        if not row:
            return None
        # Verify ownership via idea
        idea_stmt = "SELECT user_id FROM ideas WHERE id = :idea_id"
        idea = await self.db.execute(idea_stmt, {"idea_id": row.idea_id})
        if idea.scalar_one() != user_id:
            return None
        return BlueprintOut(**row)
