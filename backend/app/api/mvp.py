from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..db import get_db
from ..models import Idea, MVPBlueprint, MVPPackage
from sqlalchemy.orm import Session
import uuid
from ..utils.security import decode_token
from datetime import datetime
import boto3
import os
import json

router = APIRouter()

class MVPRequest(BaseModel):
    idea_id: uuid.UUID

class MVPResponse(BaseModel):
    mvp_id: uuid.UUID
    pdf_url: str
    download_url: str

async def get_current_user(token: str = Depends(lambda request: request.headers.get("Authorization", "").split(" ")[1]), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)
bucket = os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file_bytes: bytes, key: str) -> str:
    s3_client.put_object(Bucket=bucket, Key=key, Body=file_bytes, ContentType="application/pdf")
    return f"https://{bucket}.s3.{os.getenv('AWS_REGION','us-east-1')}.amazonaws.com/{key}"

@router.post("/", response_model=MVPResponse)
def generate_mvp(payload: MVPRequest, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user)):
    idea = db.query(Idea).filter(Idea.id == payload.idea_id, Idea.user_id == user_id).first()
    if not idea or not idea.validation_score or idea.validation_score < 0.7:
        raise HTTPException(status_code=400, detail="Idea not validated or below threshold")
    # Mock blueprint generation
    blueprint = MVPBlueprint(
        id=uuid.uuid4(),
        idea_id=idea.id,
        wireframes={"screen1": "wireframe1.png"},
        feature_list=["auth", "idea_submission"],
        tech_stack=["Python", "FastAPI", "React"],
        timeline={"setup": "1 week", "dev": "2 weeks"},
        pdf_url=""
    )
    db.add(blueprint)
    db.commit()
    db.refresh(blueprint)
    # Generate PDF placeholder
    pdf_bytes = b"%PDF-1.4\n%Mock PDF content"
    pdf_key = f"pdfs/{blueprint.id}.pdf"
    pdf_url = upload_file_to_s3(pdf_bytes, pdf_key)
    blueprint.pdf_url = pdf_url
    db.commit()
    # Generate ZIP placeholder
    zip_bytes = b"PK\x03\x04Mock ZIP content"
    zip_key = f"packages/{blueprint.id}.zip"
    zip_url = upload_file_to_s3(zip_bytes, zip_key)
    package = MVPPackage(id=uuid.uuid4(), mvp_id=blueprint.id, zip_url=zip_url)
    db.add(package)
    db.commit()
    return MVPResponse(mvp_id=blueprint.id, pdf_url=pdf_url, download_url=zip_url)

@router.get("/{mvp_id}/download")
def download_mvp(mvp_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user)):
    package = db.query(MVPPackage).join(MVPBlueprint).filter(MVPPackage.mvp_id == mvp_id, MVPBlueprint.idea_id == Idea.id, Idea.user_id == user_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"zip_url": package.zip_url}