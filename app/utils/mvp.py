import uuid
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

def generate_blueprint(description: str) -> dict:
    """Deterministically generate a simple MVP blueprint."""
    return {
        "wireframes": {"home": f"/home - {description[:20]}"},
        "features": ["login", "dashboard", "analytics"],
        "tech_stack": {"frontend": "React", "backend": "FastAPI", "db": "PostgreSQL"},
        "timeline": {"design": "1 week", "development": "2 weeks", "testing": "1 week"},
    }

def create_pdf(blueprint: dict) -> str:
    pdf_path = BASE_DIR / "storage" / f"{uuid.uuid4()}.pdf"
    with open(pdf_path, "w") as f:
        f.write("PDF placeholder for blueprint: " + json.dumps(blueprint, indent=2))
    return str(pdf_path)

def create_zip(blueprint: dict) -> str:
    zip_path = BASE_DIR / "storage" / f"{uuid.uuid4()}.zip"
    with open(zip_path, "w") as f:
        f.write("ZIP placeholder for code package: " + json.dumps(blueprint, indent=2))
    return str(zip_path)
