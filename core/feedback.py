from database.connection import get_connection


def save_feedback(analysis_id, user_id, rating, comment=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO feedbacks (analysis_id, user_id, rating, comment) VALUES (?, ?, ?, ?)",
        (analysis_id, user_id, rating, (comment or "").strip()),
    )
    conn.commit()
    conn.close()


def list_feedbacks(limit=100):
    conn = get_connection()
    rows = conn.execute(
        """SELECT f.*, u.email
           FROM feedbacks f
           LEFT JOIN users u ON u.id = f.user_id
           ORDER BY f.created_at DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]