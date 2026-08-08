import uuid
import json
import io
import zipfile
from datetime import datetime
from backend.app.services.file_storage_service import FileStorageService
from backend.app.db.models import MVPBlueprint, MVPPackage, Idea
import logging

class MVPGenerationService:
    def __init__(self):
        self.storage = FileStorageService()

    async def generate(self, idea: Idea):
        mvp_id = uuid.uuid4()
        blueprint = {
            "wireframes": [{"screen": "home", "layout": "grid"}],
            "feature_list": ["user auth", "idea submission", "validation"],
            "tech_stack": ["Python", "FastAPI", "React", "PostgreSQL"],
            "timeline": {"setup": "1 week", "dev": "2 weeks", "testing": "1 week"}
        }
        mvp = MVPBlueprint(
            id=mvp_id,
            idea_id=idea.id,
            wireframes=json.dumps(blueprint["wireframes"]),
            feature_list=json.dumps(blueprint["feature_list"]),
            tech_stack=json.dumps(blueprint["tech_stack"]),
            timeline=json.dumps(blueprint["timeline"]),
            pdf_url=None
        )
        await mvp.save()
        pdf_bytes = f"PDF for MVP {mvp_id}".encode()
        pdf_key = f"mvp/{mvp_id}/blueprint.pdf"
        pdf_url = self.storage.upload_file(pdf_bytes, pdf_key, "application/pdf")
        mvp.pdf_url = pdf_url
        await mvp.save()
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as z:
            z.writestr("README.md", f"# MVP {mvp_id}\nGenerated at {datetime.utcnow().isoformat()}")
            z.writestr("src/main.py", "print('Hello MVP')")
        zip_bytes = zip_buffer.getvalue()
        zip_key = f"mvp/{mvp_id}/package.zip"
        zip_url = self.storage.upload_file(zip_bytes, zip_key, "application/zip")
        mvp_package = MVPPackage(
            id=uuid.uuid4(),
            mvp_id=mvp_id,
            zip_url=zip_url
        )
        await mvp_package.save()
        return mvp_id, pdf_url, zip_url

    async def get_zip_url(self, mvp_id: uuid.UUID, user_id: uuid.UUID) -> str:
        mvp = await MVPBlueprint.get(id=mvp_id)
        if not mvp:
            return ""
        package = await MVPPackage.get(mvp_id=mvp_id)
        if not package:
            return ""
        return package.zip_url