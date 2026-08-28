from database.connection import get_connection


def get_user_analyses(user_id, limit=10):
    conn = get_connection()
    rows = conn.execute(
        """SELECT a.id, a.report, a.created_at, c.contract_type
           FROM analyses a LEFT JOIN contracts c ON c.id = a.contract_id
           WHERE a.user_id = ? ORDER BY a.id DESC LIMIT ?""",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]