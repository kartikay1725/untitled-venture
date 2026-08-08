"""Generate MVP blueprint and PDF.

Creates a JSON blueprint and a PDF file using fpdf.
"""

import uuid
import os
from datetime import datetime
from fpdf import FPDF

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "..", "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)


def generate_mvp(idea_id: str) -> dict:
    # Dummy blueprint data
    blueprint = {
        "wireframes": [{"screen": "Home", "layout": "grid"}],
        "feature_list": ["User signup", "Dashboard", "Analytics"],
        "tech_stack": {"frontend": "React", "backend": "FastAPI", "db": "PostgreSQL"},
        "timeline": {"design": "2w", "dev": "4w", "launch": "1w"},
    }
    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"MVP Blueprint for Idea {idea_id}", ln=True, align="C")
    pdf.ln(10)
    for key, value in blueprint.items():
        pdf.cell(200, 10, txt=f"{key.capitalize()}: {value}", ln=True)
    pdf_path = os.path.join(PDF_DIR, f"{uuid.uuid4()}.pdf")
    pdf.output(pdf_path)
    pdf_url = f"/pdfs/{os.path.basename(pdf_path)}"
    return {**blueprint, "pdf_path": pdf_path, "pdf_url": pdf_url}