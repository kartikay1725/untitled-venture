import httpx
from api.schemas import DeploymentCreate, DeploymentOut
from config import settings
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Deployment
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

class DeploymentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = httpx.AsyncClient()

    async def deploy(self, mvp_id: uuid.UUID, target: str) -> DeploymentOut:
        deployment = Deployment(
            id=uuid.uuid4(),
            mvp_id=mvp_id,
            target=target,
            status="queued",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(deployment)
        await self.db.commit()
        await self.db.refresh(deployment)
        try:
            response = await self.client.post(
                "https://deployment.service/api/deploy",
                headers={
                    "Authorization": f"Bearer {settings.DEPLOYMENT_SERVICE_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"mvp_id": str(mvp_id), "target": target},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            deployment.status = data.get("status", "success")
            deployment.url = data.get("url")
        except Exception as e:
            logger.exception("Deployment service failed")
            deployment.status = "error"
            deployment.url = None
        finally:
            deployment.updated_at = datetime.utcnow()
            self.db.add(deployment)
            await self.db.commit()
            await self.db.refresh(deployment)
        return DeploymentOut(id=deployment.id, status=deployment.status, url=deployment.url)