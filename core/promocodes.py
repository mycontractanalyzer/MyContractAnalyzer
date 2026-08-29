import secrets

from database.connection import get_connection


def create_promocode(kind="checks", value=10):
    code = secrets.token_hex(3).upper()
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO promocodes (code, kind, value, active) VALUES (?, ?, ?, 1)",
            (code, kind, value),
        )
        conn.commit()
    finally:
        conn.close()
    return code


def list_promocodes():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM promocodes ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def deactivate_promocode(code):
    conn = get_connection()
    conn.execute("UPDATE promocodes SET active = 0 WHERE code = ?", (code,))
    conn.commit()
    conn.close()


def apply_promocode(user_id, code):
    code = (code or "").strip().upper()
    if not code:
        return False, "Введите промокод"

    conn = get_connection()
    row = conn.execute("SELECT * FROM promocodes WHERE code = ? AND active = 1", (code,)).fetchone()
    if not row:
        conn.close()
        return False, "Промокод не найден или уже не активен"

    used = conn.execute(
        "SELECT 1 FROM promo_usage WHERE user_id = ? AND code = ?",
        (user_id, code),
    ).fetchone()
    if used:
        conn.close()
        return False, "Вы уже использовали этот промокод"

    if row["kind"] == "checks":
        conn.execute("UPDATE users SET checks_left = checks_left + ? WHERE id = ?", (row["value"], user_id))
    conn.execute("INSERT INTO promo_usage (user_id, code) VALUES (?, ?)", (user_id, code))
    conn.commit()
    conn.close()
    return True, f"Промокод активирован! +{row['value']} проверок."