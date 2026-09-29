import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to your .env file."
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def _build_prompt(self, document_type, parties, terms, dates,
                      additional_instructions, language):
        return f'''
You are LegalEase, an AI assistant for drafting legal-document drafts.

Create a professional, structured draft for this request.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE / DATES:
{dates}

TERMS AND CONDITIONS:
{terms}

ADDITIONAL INSTRUCTIONS:
{additional_instructions or "None"}

OUTPUT LANGUAGE:
{language}

Requirements:
1. Produce only the document draft, without meta commentary.
2. Use clear headings and numbered sections.
3. Include parties, effective date, definitions where useful, obligations,
   payment/consideration where applicable, confidentiality where relevant,
   termination, dispute/governing-law placeholders where appropriate,
   notices, signatures and other standard sections suitable for the document.
4. Do not invent facts the user did not provide.
5. For missing legal details, use placeholders such as [GOVERNING LAW].
6. Keep the language professional and editable.
7. This is a drafting aid, not legal advice.
'''

    def generate_document(self, document_type, parties, terms, dates,
                          additional_instructions="", language="English"):
        prompt = self._build_prompt(
            document_type, parties, terms, dates,
            additional_instructions, language
        )
        response = self.model.generate_content(prompt)
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
