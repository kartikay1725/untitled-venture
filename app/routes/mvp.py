from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import async_session
from app.models import MVPTemplate, Idea
from app.schemas import MVPCreate, MVPOut
from app.services.mvp_service import MVPService
from app.utils.security import get_current_user
import uuid
import logging

router = APIRouter()

@router.post("/", response_model=MVPOut)
async def create_mvp(mvp_in: MVPCreate, token=Depends(get_current_user)):
    async with async_session() as session:
        idea_res = await session.execute(select(Idea).where(Idea.id == mvp_in.ideaId, Idea.user_id == token.user_id))
        idea = idea_res.scalars().first()
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")
        mvp = MVPTemplate(
            id=uuid.uuid4(),
            idea_id=idea.id,
            features=mvp_in.features,
            status="pending"
        )
        session.add(mvp)
        await session.commit()
        await session.refresh(mvp)
        service = MVPService()
        code = await service.generate_code(mvp.features)
        mvp.generated_code = code
        mvp.status = "ready"
        await session.commit()
        await session.refresh(mvp)
        return MVPOut(
            mvpId=mvp.id,
            status=mvp.status,
            generatedCode=mvp.generated_code
        )

@router.get("/{mvp_id}", response_model=MVPOut)
async def get_mvp(mvp_id: uuid.UUID, token=Depends(get_current_user)):
    async with async_session() as session:
        res = await session.execute(select(MVPTemplate).where(MVPTemplate.id == mvp_id, MVPTemplate.idea_id == token.user_id))
        mvp = res.scalars().first()
        if not mvp:
            raise HTTPException(status_code=404, detail="MVP not found")
        return MVPOut(
            mvpId=mvp.id,
            status=mvp.status,
            generatedCode=mvp.generated_code
        )
