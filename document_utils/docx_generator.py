from io import BytesIO
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

ASSETS = Path(__file__).resolve().parent.parent / "assets"

def format_docx(text: str, doc_type: str) -> bytes:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    logo = ASSETS / "logo.png"
    if logo.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(logo), width=Inches(1.2))

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(doc_type.upper())
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            doc.add_paragraph()
            continue

        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)

        is_heading = (
            line.startswith("#")
            or (line.isupper() and len(line) < 100)
            or line.endswith(":")
        )
        r = p.add_run(line.lstrip("# ").strip())
        r.font.name = "Times New Roman"
        r.font.size = Pt(12 if is_heading else 11)
        r.bold = is_heading

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer.add_run("LegalEase - AI-generated legal draft")
    footer_run.font.name = "Times New Roman"
    footer_run.font.size = Pt(8)

    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()
