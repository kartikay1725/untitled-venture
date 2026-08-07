from fastapi import APIRouter, Depends, HTTPException
from api.schemas import MVPCreate, MVPOut
from api.services.mvp_service import MVPService
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from api.models import MVPTemplate
from sqlalchemy import select

router = APIRouter(prefix="/mvp", tags=["mvp"])

@router.post("/", response_model=MVPOut)
async def generate_mvp(mvp_in: MVPCreate, db: AsyncSession = Depends(get_db)):
    service = MVPService(db)
    mvp = await service.generate(mvp_in.idea_id, mvp_in.features)
    return mvp

@router.get("/{mvp_id}", response_model=MVPOut)
async def get_mvp(mvp_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MVPTemplate).where(MVPTemplate.id == mvp_id))
    mvp = result.scalar_one_or_none()
    if not mvp:
        raise HTTPException(status_code=404, detail="MVP not found")
    return MVPOut(id=mvp.id, status=mvp.status, generated_code=mvp.generated_code)