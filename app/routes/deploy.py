from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import async_session
from app.models import Deployment, MVPTemplate
from app.schemas import DeploymentCreate, DeploymentOut
from app.services.deployment_service import DeploymentService
from app.utils.security import get_current_user
import uuid
import logging

router = APIRouter()

@router.post("/", response_model=DeploymentOut)
async def create_deployment(deploy_in: DeploymentCreate, token=Depends(get_current_user)):
    async with async_session() as session:
        mvp_res = await session.execute(select(MVPTemplate).where(MVPTemplate.id == deploy_in.mvpId, MVPTemplate.idea_id == token.user_id))
        mvp = mvp_res.scalars().first()
        if not mvp or mvp.status != "ready":
            raise HTTPException(status_code=400, detail="MVP not ready")
        deployment = Deployment(
            id=uuid.uuid4(),
            mvp_id=mvp.id,
            target=deploy_in.target,
            status="queued"
        )
        session.add(deployment)
        await session.commit()
        await session.refresh(deployment)
        service = DeploymentService()
        url = await service.deploy(deployment.target, mvp.generated_code)
        deployment.url = url
        deployment.status = "success"
        await session.commit()
        await session.refresh(deployment)
        return DeploymentOut(
            deploymentId=deployment.id,
            status=deployment.status,
            url=deployment.url
        )

@router.get("/{deployment_id}", response_model=DeploymentOut)
async def get_deployment(deployment_id: uuid.UUID, token=Depends(get_current_user)):
    async with async_session() as session:
        res = await session.execute(select(Deployment).where(Deployment.id == deployment_id))
        deployment = res.scalars().first()
        if not deployment:
            raise HTTPException(status_code=404, detail="Deployment not found")
        return DeploymentOut(
            deploymentId=deployment.id,
            status=deployment.status,
            url=deployment.url
        )
