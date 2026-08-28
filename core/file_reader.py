import pdfplumber


def read_uploaded_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()

    if name.endswith((".txt", ".md")):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        parts = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                parts.append(page.extract_text() or "")
        return "\n".join(parts)

    raise ValueError("Неподдерживаемый формат файла")