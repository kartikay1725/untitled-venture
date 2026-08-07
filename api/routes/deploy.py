from fastapi import APIRouter, Depends, HTTPException
from api.schemas import DeploymentCreate, DeploymentOut
from api.services.deployment_service import DeploymentService
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from api.models import Deployment
from sqlalchemy import select

router = APIRouter(prefix="/deploy", tags=["deploy"])

@router.post("/", response_model=DeploymentOut)
async def deploy(deploy_in: DeploymentCreate, db: AsyncSession = Depends(get_db)):
    service = DeploymentService(db)
    deployment = await service.deploy(deploy_in.mvp_id, deploy_in.target)
    return deployment

@router.get("/{deployment_id}", response_model=DeploymentOut)
async def get_deployment(deployment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Deployment).where(Deployment.id == deployment_id))
    deployment = result.scalar_one_or_none()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return DeploymentOut(id=deployment.id, status=deployment.status, url=deployment.url)