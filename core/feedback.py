from database.connection import get_connection


def upsert_feedback(analysis_id, user_id, rating, comment=""):
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM feedbacks WHERE user_id = ? AND analysis_id = ?",
        (user_id, analysis_id),
    ).fetchone()
    if row:
        conn.execute(
            "UPDATE feedbacks SET rating = ?, comment = ?, created_at = CURRENT_TIMESTAMP WHERE id = ?",
            (rating, (comment or "").strip(), row["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO feedbacks (analysis_id, user_id, rating, comment) VALUES (?, ?, ?, ?)",
            (analysis_id, user_id, rating, (comment or "").strip()),
        )
    conn.commit()
    conn.close()


def get_feedback(user_id, analysis_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM feedbacks WHERE user_id = ? AND analysis_id = ?",
        (user_id, analysis_id),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


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