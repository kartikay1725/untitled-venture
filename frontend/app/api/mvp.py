"""MVP generation and download routes.

POST /api/mvp creates a blueprint and returns PDF and download URLs.
GET /api/mvp/{mvp_id}/download returns the ZIP URL.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
import os

from app.database import get_db
from app.models import MVPBlueprint, MVPPackage
from app.services.mvp_generation_service import generate_mvp

router = APIRouter()

class MVPRequest(BaseModel):
    idea_id: str

class MVPResponse(BaseModel):
    mvp_id: str
    pdf_url: str
    download_url: str

@router.post("", response_model=MVPResponse)
async def create_mvp(req: MVPRequest, db: Session = Depends(get_db)):
    blueprint = generate_mvp(req.idea_id)
    mvp = MVPBlueprint(
        idea_id=uuid.UUID(req.idea_id),
        wireframes=blueprint["wireframes"],
        feature_list=blueprint["feature_list"],
        tech_stack=blueprint["tech_stack"],
        timeline=blueprint["timeline"],
        pdf_url=blueprint["pdf_path"],
    )
    db.add(mvp)
    db.commit()
    db.refresh(mvp)
    # Create ZIP package
    zip_path = os.path.join("packages", f"{mvp.id}.zip")
    # For demo, just copy PDF into ZIP (real logic omitted)
    import shutil, zipfile
    os.makedirs("packages", exist_ok=True)
    shutil.copy(blueprint["pdf_path"], zip_path)
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(blueprint["pdf_path"], arcname=os.path.basename(blueprint["pdf_path"]))
    package = MVPPackage(mvp_id=mvp.id, zip_url=zip_path)
    db.add(package)
    db.commit()
    db.refresh(package)
    return MVPResponse(
        mvp_id=str(mvp.id),
        pdf_url=blueprint["pdf_url"],
        download_url=f"/api/mvp/{mvp.id}/download",
    )

@router.get("/{mvp_id}/download")
async def download_package(mvp_id: str, db: Session = Depends(get_db)):
    package = db.query(MVPPackage).filter(MVPPackage.mvp_id == uuid.UUID(mvp_id)).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"zip_url": package.zip_url}