from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Idea, MVPBlueprint, MVPPackage
from app.utils.settings import Settings
from app.db import get_db, get_current_user
from app.services.mvp_generation import generate_mvp
from app.services.file_storage import upload_file
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter()
settings = Settings()

class MVPRequest(BaseModel):
    idea_id: str

class MVPResponse(BaseModel):
    mvp_id: str
    pdf_url: str
    download_url: str

@router.post("", response_model=MVPResponse)
async def create_mvp(req: MVPRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Idea).where(Idea.id == req.idea_id, Idea.user_id == user.id))
    idea = result.scalar_one_or_none()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.validation_score < 70:
        raise HTTPException(status_code=400, detail="Idea not viable")
    blueprint = generate_mvp(idea.description)
    mvp = MVPBlueprint(idea_id=idea.id, wireframes=blueprint['wireframes'], feature_list=blueprint['features'], tech_stack=blueprint['tech_stack'], timeline=blueprint['timeline'])
    db.add(mvp)
    await db.commit()
    await db.refresh(mvp)
    pdf_bytes = blueprint['pdf']
    pdf_url = await upload_file(f"{mvp.id}.pdf", pdf_bytes, "pdf")
    mvp.pdf_url = pdf_url
    await db.commit()
    await db.refresh(mvp)
    return MVPResponse(mvp_id=str(mvp.id), pdf_url=pdf_url, download_url=f"/api/mvp/{mvp.id}/download")

@router.get("{mvp_id}/download")
async def download_mvp(mvp_id: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(MVPBlueprint).where(MVPBlueprint.id == mvp_id))
    mvp = result.scalar_one_or_none()
    if not mvp:
        raise HTTPException(status_code=404, detail="MVP not found")
    # For simplicity, return the PDF URL; real implementation would stream ZIP
    return {"zip_url": mvp.pdf_url}
