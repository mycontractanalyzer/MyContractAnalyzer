from database.connection import get_connection


def save_highlights(analysis_id, payload):
    conn = get_connection()
    conn.execute("UPDATE analyses SET highlights = ? WHERE id = ?", (payload, analysis_id))
    conn.commit()
    conn.close()


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