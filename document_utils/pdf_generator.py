from pathlib import Path
from fpdf import FPDF
from document_utils.sanitizer import sanitize_text

ASSETS = Path(__file__).resolve().parent.parent / "assets"

class LegalPDF(FPDF):
    def __init__(self, doc_type):
        super().__init__()
        self.doc_type = doc_type
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        logo = ASSETS / "logo.png"
        if logo.exists():
            try:
                self.image(str(logo), x=95, y=8, w=20)
                self.ln(18)
            except Exception:
                pass
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 8, self.doc_type.upper(), align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", size=8)
        self.cell(0, 8, "LegalEase - AI-generated legal draft", align="C")

def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = LegalPDF(doc_type)
    pdf.add_page()

    for raw in sanitize_text(text).splitlines():
        line = raw.strip()
        if not line:
            pdf.ln(3)
            continue

        if line.startswith("#") or (line.isupper() and len(line) < 100):
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, line.lstrip("# ").strip())
        elif line.startswith(("-", "*", "•")):
            pdf.set_font("Helvetica", size=10)
            pdf.multi_cell(0, 5, "• " + line.lstrip("-*• ").strip())
        else:
            pdf.set_font("Helvetica", size=10)
            pdf.multi_cell(0, 5, line)

        pdf.ln(1)

    return bytes(pdf.output())
