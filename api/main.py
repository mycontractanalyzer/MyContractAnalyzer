"""MyContractAnalyzer API — шаг 1 переезда. Работает параллельно со Streamlit."""
import json

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import secrets as py_secrets

from core.analyzer import analyze_contract_stream, split_report_highlights
from core.contracts import save_analysis, save_contract, spend_checks
from core.mailer import send_code_email
from core.records import save_highlights
from database.connection import get_connection
from utils.auth import hash_password, is_valid_email, verify_password

app = FastAPI(title="MyContractAnalyzer API", version="1.0")


class RegisterIn(BaseModel):
    email: str
    password: str
    password2: str


class VerifyIn(BaseModel):
    email: str
    code: str


class LoginIn(BaseModel):
    email: str
    password: str


class AnalyzeIn(BaseModel):
    text: str
    depth: str = "standard"
    contract_type: str = ""
    role: str = ""
    comment: str = ""


def _user_by_token(token: str):
    if not token:
        return None
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
    conn.close()
    return dict(row) if row else None


def _auth(authorization: str = Header(default="")):
    user = _user_by_token(authorization.replace("Bearer ", "").strip())
    if not user:
        raise HTTPException(401, "Не авторизован")
    return user


@app.get("/api/health")
def health():
    return {"ok": True, "service": "mca-api"}


@app.post("/api/register")
def register(data: RegisterIn):
    email = data.email.strip().lower()
    if not is_valid_email(email):
        raise HTTPException(400, "Некорректный email")
    if len(data.password or "") < 6:
        raise HTTPException(400, "Пароль должен быть не короче 6 символов")
    if data.password != data.password2:
        raise HTTPException(400, "Пароли не совпадают")
    conn = get_connection()
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
    if "verified" not in cols:
        conn.execute("ALTER TABLE users ADD COLUMN verified INTEGER DEFAULT 0")
        conn.execute("ALTER TABLE users ADD COLUMN verify_code TEXT DEFAULT ''")
        conn.commit()
    try:
        conn.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)",
                     (email, hash_password(data.password)))
        conn.commit()
    except Exception:
        conn.close()
        raise HTTPException(409, "Пользователь с таким email уже существует")
    code = str(py_secrets.randbelow(900000) + 100000)
    conn.execute("UPDATE users SET verified = 0, verify_code = ? WHERE email = ?", (code, email))
    conn.commit()
    conn.close()
    send_code_email(email, code)
    return {"ok": True, "message": "Код подтверждения отправлен на почту"}


@app.post("/api/verify")
def verify(data: VerifyIn):
    email = data.email.strip().lower()
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if row and (row["verify_code"] or "") == data.code.strip():
        conn.execute("UPDATE users SET verified = 1, verify_code = '' WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return {"ok": True}
    conn.close()
    raise HTTPException(400, "Неверный код")


@app.post("/api/login")
def login(data: LoginIn):
    email = data.email.strip().lower()
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if row is None or not verify_password(data.password, row["password_hash"]):
        conn.close()
        raise HTTPException(401, "Неверный email или пароль")
    if not row["verified"]:
        conn.close()
        raise HTTPException(403, "Почта не подтверждена")
    token = py_secrets.token_hex(16)
    conn.execute("UPDATE users SET token = ? WHERE id = ?", (token, row["id"]))
    conn.commit()
    conn.close()
    return {"ok": True, "token": token}


@app.get("/api/me")
def me(user=Depends(_auth)):
    return {"email": user["email"], "tariff": user["tariff"], "checks_left": user["checks_left"]}


@app.post("/api/analyze")
def analyze(data: AnalyzeIn, user=Depends(_auth)):
    if user["checks_left"] < 1:
        raise HTTPException(402, "Недостаточно проверок")
    gen, model = analyze_contract_stream(
        data.text, user["tariff"], data.contract_type, data.role, data.comment, depth=data.depth)

    def stream():
        chunks = []
        for ch in gen:
            chunks.append(ch)
            yield f"data: {json.dumps({'chunk': ch}, ensure_ascii=False)}\n\n"
        report, hl = split_report_highlights("".join(chunks))
        spend_checks(user["id"], len(data.text))
        cid = save_contract(user["id"], data.contract_type or "Договор", data.role, data.text)
        aid = save_analysis(user["id"], cid, model, report)
        if hl:
            save_highlights(aid, hl)
        yield f"data: {json.dumps({'done': True, 'analysis_id': aid}, ensure_ascii=False)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/api/analyses")
def analyses(user=Depends(_auth)):
    conn = get_connection()
    rows = conn.execute(
        "SELECT a.id, a.created_at, a.report, c.contract_type "
        "FROM analyses a JOIN contracts c ON c.id = a.contract_id "
        "WHERE a.user_id = ? ORDER BY a.id DESC LIMIT 30", (user["id"],)).fetchall()
    conn.close()
    return [{"id": r["id"], "created_at": r["created_at"], "type": r["contract_type"],
             "preview": (r["report"] or "")[:120]} for r in rows]


@app.get("/api/analyses/{aid}")
def analysis_detail(aid: int, user=Depends(_auth)):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM analyses WHERE id = ? AND user_id = ?", (aid, user["id"])).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Отчёт не найден")
    return {"id": row["id"], "report": row["report"],
            "highlights": row["highlights"], "created_at": row["created_at"]}


class _FileShim:
    """Обёртка, чтобы переиспользовать ридер файлов из Streamlit-версии."""
    def __init__(self, name, mime, data):
        self.name = name
        self.type = mime
        self._data = data

    def read(self):
        return self._data

    def getvalue(self):
        return self._data


@app.post("/api/upload")
async def upload(file: UploadFile = File(...), user=Depends(_auth)):
    data = await file.read()
    name = (file.filename or "").lower()
    text = ""
    try:
        from core.file_reader import read_uploaded_file
        text = read_uploaded_file(_FileShim(file.filename, file.content_type or "", data)) or ""
    except Exception:
        text = ""
    if not text.strip():
        import io
        if name.endswith((".txt", ".md")):
            text = data.decode("utf-8", errors="ignore")
        elif name.endswith(".pdf"):
            try:
                import pdfplumber
                with pdfplumber.open(io.BytesIO(data)) as pdf:
                    text = "\n".join((p.extract_text() or "") for p in pdf.pages)
            except Exception:
                try:
                    from pypdf import PdfReader
                except Exception:
                    from PyPDF2 import PdfReader
                reader = PdfReader(io.BytesIO(data))
                text = "\n".join((p.extract_text() or "") for p in reader.pages)
        elif name.endswith(".docx"):
            import docx
            d = docx.Document(io.BytesIO(data))
            parts = [p.text for p in d.paragraphs]
            for t in d.tables:
                for row in t.rows:
                    parts.append(" ".join(c.text for c in row.cells))
            text = "\n".join(parts)
        else:
            raise HTTPException(400, "Форматы: TXT, MD, PDF, DOCX")
    if not text.strip():
        raise HTTPException(400, "В файле нет текста (возможно, это скан — используй старую версию с OCR)")
    return {"ok": True, "text": text, "chars": len(text)}