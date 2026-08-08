import json
import uuid
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
class MVPBlueprint:
    def __init__(self, wireframes, feature_list, tech_stack, timeline, pdf_url):
        self.wireframes = wireframes
        self.feature_list = feature_list
        self.tech_stack = tech_stack
        self.timeline = timeline
        self.pdf_url = pdf_url
class MVPGenerationService:
    @staticmethod
    def generate(idea):
        wireframes = [{"screen": "Home", "layout": "simple"}]
        feature_list = [{"name": "Login", "type": "auth"}]
        tech_stack = {"frontend": "Next.js", "backend": "FastAPI", "db": "PostgreSQL"}
        timeline = {"planning": "1 week", "development": "2 weeks", "testing": "1 week"}
        pdf_path = Path(f"pdfs/{uuid.uuid4()}.pdf")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.drawString(100, 750, f"MVP Blueprint for {idea.description[:30]}...")
        c.save()
        pdf_url = f"/static/{pdf_path.name}"
        return MVPBlueprint(json.dumps(wireframes), json.dumps(feature_list), json.dumps(tech_stack), json.dumps(timeline), pdf_url)