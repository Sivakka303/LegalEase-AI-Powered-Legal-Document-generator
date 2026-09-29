# LegalEase — AI-Powered Legal Document Generator

Complete FastAPI + Streamlit + Gemini project.

## Features
- AI legal-document draft generation
- Employment contracts, NDAs, lease agreements, service agreements, etc.
- Editable preview
- TXT / DOCX / PDF downloads
- Optional logo branding
- FastAPI `/generate` endpoint
- Environment-variable based Gemini API configuration

## Run on Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your Gemini API key.

Terminal 1:
```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2:
```powershell
streamlit run frontend/app.py
```

Backend: http://127.0.0.1:8000
Frontend: http://localhost:8501

Optional logo:
`assets/logo.png`

Important: generated documents are drafting aids, not a substitute for review by a qualified legal professional.
