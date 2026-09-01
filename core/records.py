from datetime import datetime, timedelta

from database.connection import get_connection


def save_highlights(analysis_id, payload):
    conn = get_connection()
    conn.execute("UPDATE analyses SET highlights = ? WHERE id = ?", (payload, analysis_id))
    conn.commit()
    conn.close()


def rename_analysis(analysis_id, title):
    conn = get_connection()
    conn.execute("UPDATE analyses SET title = ? WHERE id = ?", ((title or "").strip() or "Договор", analysis_id))
    conn.commit()
    conn.close()


def fmt_dt(s):
    """2026-08-31 16:35:04 (UTC) -> 31-08-2026 19:35 (МСК)"""
    try:
        dt = datetime.fromisoformat(str(s)[:19]) + timedelta(hours=3)
        return dt.strftime("%d-%m-%Y %H:%M")
    except Exception:
        return str(s)


def save_consult_request(user_id, analysis_id, question, contact):
    conn = get_connection()
    conn.execute(
        "INSERT INTO consult_requests (user_id, analysis_id, question, contact) VALUES (?, ?, ?, ?)",
        (user_id, analysis_id, (question or "").strip(), (contact or "").strip()),
    )
    conn.commit()
    conn.close()


def list_consults(limit=200):
    conn = get_connection()
    rows = conn.execute(
        """SELECT c.*, u.email
           FROM consult_requests c
           LEFT JOIN users u ON u.id = c.user_id
           ORDER BY c.created_at DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
def save_checklist(analysis_id, payload):
    conn = get_connection()
    conn.execute("UPDATE analyses SET checklist = ? WHERE id = ?", (payload, analysis_id))
    conn.commit()
    conn.close()


def set_share(analysis_id, on=1):
    conn = get_connection()
    conn.execute("UPDATE analyses SET share = ? WHERE id = ?", (int(on), analysis_id))
    conn.commit()
    conn.close()