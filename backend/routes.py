from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=5000)
    terms: str = Field(..., min_length=2, max_length=10000)
    dates: str = Field(..., min_length=2, max_length=200)
    additional_instructions: str = Field(default="", max_length=5000)
    language: str = Field(default="English", max_length=50)

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
            additional_instructions=request.additional_instructions,
            language=request.language,
        )
        return {
            "success": True,
            "document_type": request.document_type,
            "content": text,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
