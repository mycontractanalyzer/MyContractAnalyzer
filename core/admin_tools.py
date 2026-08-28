from datetime import datetime, timedelta

from database.connection import get_connection
from core.tariffs import TARIFFS


def list_users():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, email, tariff, checks_left, subscription_end FROM users ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_user(email):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email.strip().lower(),)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def add_checks(user_id, n):
    conn = get_connection()
    conn.execute("UPDATE users SET checks_left = checks_left + ? WHERE id = ?", (n, user_id))
    conn.commit()
    conn.close()


def grant_tariff(user_id, tariff, months):
    checks = TARIFFS[tariff]["checks"]
    end = datetime.now() + timedelta(days=30 * months)
    conn = get_connection()
    conn.execute(
        "UPDATE users SET tariff = ?, checks_left = ?, subscription_end = ? WHERE id = ?",
        (tariff, checks, end.strftime("%Y-%m-%d %H:%M"), user_id),
    )
    conn.commit()
    conn.close()