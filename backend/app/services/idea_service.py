import uuid
from ..database.engine import get_session
from ..api.models import Idea
from ..api.schemas import IdeaCreateRequest, IdeaResponse
from fastapi import HTTPException
from sqlalchemy import select

class IdeaService:
    @staticmethod
    async def create_idea(user_id: uuid.UUID, title: str, description: str) -> IdeaResponse:
        async with get_session() as session:
            idea = Idea(id=uuid.uuid4(), user_id=user_id, title=title, description=description, status="pending")
            session.add(idea)
            await session.commit()
            await session.refresh(idea)
            return IdeaResponse(id=idea.id, title=idea.title, description=idea.description, submitted_at=idea.submitted_at.isoformat(), status=idea.status)
