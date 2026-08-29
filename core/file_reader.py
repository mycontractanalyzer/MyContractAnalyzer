import pdfplumber
from docx import Document


def read_uploaded_file(uploaded) -> str:
    name = (uploaded.name or "").lower()

    if name.endswith((".txt", ".md")):
        return uploaded.read().decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        parts = []
        with pdfplumber.open(uploaded) as pdf:
            for page in pdf.pages:
                parts.append(page.extract_text() or "")
        return "\n".join(parts)

    if name.endswith(".docx"):
        doc = Document(uploaded)
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError("Неподдерживаемый формат файла")