import httpx
from api.schemas import MVPCreate, MVPOut
from config import settings
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import MVPTemplate
from sqlalchemy import select
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class MVPService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = httpx.AsyncClient()

    async def generate(self, idea_id: uuid.UUID, features: list[str]) -> MVPOut:
        mvp = MVPTemplate(
            id=uuid.uuid4(),
            idea_id=idea_id,
            features=features,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(mvp)
        await self.db.commit()
        await self.db.refresh(mvp)
        prompt = f"Generate a minimal Next.js 14 project skeleton with the following features: {', '.join(features)}. Return the code as a single string."
        try:
            response = await self.client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000,
                    "temperature": 0.5
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            code = data["choices"][0]["message"]["content"]
            mvp.generated_code = code
            mvp.status = "ready"
        except Exception as e:
            logger.exception("OpenAI MVP generation failed")
            mvp.status = "failed"
            mvp.generated_code = None
        finally:
            mvp.updated_at = datetime.utcnow()
            self.db.add(mvp)
            await self.db.commit()
            await self.db.refresh(mvp)
        return MVPOut(id=mvp.id, status=mvp.status, generated_code=mvp.generated_code)