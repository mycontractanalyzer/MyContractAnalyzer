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


def _ensure_usage_table(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS lawyer_usage (
        user_id INTEGER, day TEXT, cnt INTEGER DEFAULT 0,
        PRIMARY KEY(user_id, day))""")


def get_lawyer_count(user_id):
    conn = get_connection()
    _ensure_usage_table(conn)
    row = conn.execute(
        "SELECT cnt FROM lawyer_usage WHERE user_id = ? AND day = ?",
        (user_id, datetime.now().strftime("%Y-%m-%d")),
    ).fetchone()
    conn.close()
    return row["cnt"] if row else 0


def bump_lawyer_usage(user_id, limit):
    """Возвращает (разрешено, текущий счётчик)."""
    day = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    _ensure_usage_table(conn)
    row = conn.execute("SELECT cnt FROM lawyer_usage WHERE user_id = ? AND day = ?", (user_id, day)).fetchone()
    cnt = row["cnt"] if row else 0
    if cnt >= limit:
        conn.close()
        return False, cnt
    if row:
        conn.execute("UPDATE lawyer_usage SET cnt = cnt + 1 WHERE user_id = ? AND day = ?", (user_id, day))
    else:
        conn.execute("INSERT INTO lawyer_usage (user_id, day, cnt) VALUES (?, ?, 1)", (user_id, day))
    conn.commit()
    conn.close()
    return True, cnt + 1