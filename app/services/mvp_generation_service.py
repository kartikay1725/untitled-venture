import uuid
import base64
import json
import os
from datetime import datetime
from typing import Dict
from app.models import MVPBlueprint, MVPPackage
from app.services.file_storage_service import upload_file_to_s3
from app.db import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.exceptions import ExternalAPIError
import httpx

MVP_GENERATION_API_URL = os.getenv("MVP_GENERATION_API_URL", "https://api.example.com/generate")
MVP_GENERATION_TIMEOUT = 10.0

async def generate_mvp(idea_id: uuid.UUID) -> Dict:
    async with httpx.AsyncClient(timeout=MVP_GENERATION_TIMEOUT) as client:
        try:
            response = await client.post(MVP_GENERATION_API_URL, json={"idea_id": str(idea_id)})
            response.raise_for_status()
            data = response.json()
            pdf_content = data.get("pdf_content")
            if not pdf_content:
                raise ValueError("Missing PDF content")
            pdf_bytes = base64.b64decode(pdf_content)
            pdf_url = await upload_file_to_s3(pdf_bytes, f"mvp/{idea_id}/blueprint.pdf")
            mvp = MVPBlueprint(
                idea_id=idea_id,
                wireframes=data.get("wireframes"),
                feature_list=data.get("feature_list"),
                tech_stack=data.get("tech_stack"),
                timeline=data.get("timeline"),
                pdf_url=pdf_url,
                created_at=datetime.utcnow()
            )
            async with async_session() as session:
                session.add(mvp)
                await session.commit()
                await session.refresh(mvp)
            zip_bytes = await create_zip_package(mvp.id)
            zip_url = await upload_file_to_s3(zip_bytes, f"mvp/{idea_id}/package.zip")
            package = MVPPackage(mvp_id=mvp.id, zip_url=zip_url, generated_at=datetime.utcnow())
            async with async_session() as session:
                session.add(package)
                await session.commit()
                await session.refresh(package)
            return {"mvp_id": str(mvp.id), "pdf_url": pdf_url, "download_url": zip_url}
        except httpx.HTTPStatusError as exc:
            raise ExternalAPIError(f"MVP generation API error: {exc}") from exc
        except httpx.RequestError as exc:
            raise ExternalAPIError(f"MVP generation request error: {exc}") from exc
        except (ValueError, KeyError) as exc:
            raise ExternalAPIError(f"Invalid MVP generation response: {exc}") from exc

async def create_zip_package(mvp_id: uuid.UUID) -> bytes:
    import zipfile
    import io
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("README.md", f"# MVP Package {mvp_id}")
    return buffer.getvalue()