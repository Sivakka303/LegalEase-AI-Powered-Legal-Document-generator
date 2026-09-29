import os
import requests
import streamlit as st
from dotenv import load_dotenv

from document_utils.docx_generator import format_docx
from document_utils.pdf_generator import format_pdf
from document_utils.html_preview import format_html_preview
from document_utils.sanitizer import sanitize_text

load_dotenv()

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "edited_text" not in st.session_state:
    st.session_state.edited_text = ""
if "document_type" not in st.session_state:
    st.session_state.document_type = "Employment Contract"

st.markdown("""
<style>
.main-title {text-align:center; font-size:42px; font-weight:700;}
.subtitle {text-align:center; color:#6b7280; margin-bottom:25px;}
</style>
""", unsafe_allow_html=True)

logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image(logo_path, width=110)

st.markdown('<div class="main-title">LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

st.info(
    "LegalEase creates editable legal-document drafts. Review important "
    "documents with a qualified legal professional before signing."
)

with st.form("legal_form"):
    left, right = st.columns(2)

    with left:
        document_type = st.selectbox(
            "Document Type",
            [
                "Employment Contract",
                "Non-Disclosure Agreement (NDA)",
                "Lease Agreement",
                "Service Agreement",
                "Freelance Work Contract",
                "Employment Offer Letter",
                "General Agreement",
            ],
        )
        parties = st.text_area(
            "Parties Involved",
            placeholder="Jane Doe (Employee), ABC Technologies (Employer)",
            height=120,
        )

    with right:
        dates = st.text_input(
            "Effective Date / Dates",
            placeholder="April 15, 2026",
        )
        language = st.selectbox(
            "Output Language",
            ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"],
        )

    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Use semicolons for clauses: Salary is paid monthly; "
            "confidentiality must be maintained; either party may terminate "
            "with 30 days notice"
        ),
        height=180,
    )

    additional = st.text_area(
        "Additional Instructions (optional)",
        placeholder="Special clauses, formatting preferences, placeholders, etc.",
        height=100,
    )

    submitted = st.form_submit_button(
        "Generate Document",
        use_container_width=True,
        type="primary",
    )

if submitted:
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please fill Document Type, Parties, Terms and Effective Date.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
            "additional_instructions": additional,
            "language": language,
        }

        with st.spinner("Generating your legal document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )

                if response.ok:
                    result = response.json()
                    generated = sanitize_text(result["content"])
                    st.session_state.generated_text = generated
                    st.session_state.edited_text = generated
                    st.session_state.document_type = document_type
                    st.success("Document generated successfully.")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(f"Backend error: {detail}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "FastAPI is not running. Start it with: "
                    "uvicorn backend.main:app --reload --port 8000"
                )
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")

if st.session_state.generated_text:
    st.divider()
    st.subheader("Document Preview")

    tab1, tab2 = st.tabs(["Preview", "Edit Document"])

    with tab1:
        st.markdown(
            format_html_preview(st.session_state.edited_text),
            unsafe_allow_html=True,
        )

    with tab2:
        edited = st.text_area(
            "Edit the generated document",
            value=st.session_state.edited_text,
            height=650,
        )
        if st.button("Save Edits"):
            st.session_state.edited_text = sanitize_text(edited)
            st.success("Edits saved.")

    st.divider()
    st.subheader("Download")

    final_text = st.session_state.edited_text
    doc_type = st.session_state.document_type
    safe_name = "".join(
        ch.lower() if ch.isalnum() else "_"
        for ch in doc_type
    ).strip("_")

    b1, b2, b3 = st.columns(3)

    with b1:
        st.download_button(
            "Download TXT",
            data=final_text.encode("utf-8"),
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with b2:
        st.download_button(
            "Download DOCX",
            data=format_docx(final_text, doc_type),
            file_name=f"{safe_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

    with b3:
        st.download_button(
            "Download PDF",
            data=format_pdf(final_text, doc_type),
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.caption("LegalEase | FastAPI + Streamlit + Google Gemini")
