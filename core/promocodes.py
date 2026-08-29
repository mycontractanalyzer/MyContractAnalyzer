import secrets
import sqlite3
from datetime import datetime

from database.connection import get_connection


def create_promocode(kind="checks", value=10, discount_rub=0, min_tariff=None,
                     checks_bonus=0, expires_at=None, custom_code=None):
    if custom_code:
        code = custom_code.strip().upper().replace(" ", "")
        if not code:
            return False, "Код не может быть пустым"
        if len(code) > 30:
            return False, "Код слишком длинный (максимум 30 символов)"
    else:
        code = secrets.token_hex(3).upper()

    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO promocodes
               (code, kind, value, discount_rub, min_tariff, checks_bonus, expires_at, used_count, active)
               VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1)""",
            (code, kind, int(value), int(discount_rub), min_tariff, int(checks_bonus), expires_at),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False, f"Промокод с кодом «{code}» уже существует"
    conn.close()
    return True, code


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


def apply_promocode_checks(user_id, code):
    """Промокод на проверки: счётчик растёт только при реальном зачислении."""
    code = (code or "").strip().upper()
    if not code:
        return False, "Введите промокод"

    conn = get_connection()
    row = conn.execute("SELECT * FROM promocodes WHERE code = ? AND active = 1", (code,)).fetchone()
    if not row:
        conn.close()
        return False, "Промокод не найден или уже не активен"

    if row["expires_at"] and datetime.fromisoformat(row["expires_at"]) < datetime.now():
        conn.close()
        return False, "Срок действия промокода истёк"

    if row["kind"] != "checks" and (row["checks_bonus"] or 0) <= 0:
        conn.close()
        return False, "Этот промокод не даёт проверки (он на скидку)"

    if conn.execute("SELECT 1 FROM promo_usage WHERE user_id = ? AND code = ?", (user_id, code)).fetchone():
        conn.close()
        return False, "Вы уже использовали этот промокод"

    bonus = row["checks_bonus"] if row["checks_bonus"] else row["value"]
    conn.execute("UPDATE users SET checks_left = checks_left + ? WHERE id = ?", (bonus, user_id))
    conn.execute("INSERT INTO promo_usage (user_id, code) VALUES (?, ?)", (user_id, code))
    conn.execute("UPDATE promocodes SET used_count = used_count + 1 WHERE code = ?", (code,))
    conn.commit()
    conn.close()
    return True, f"Промокод активирован! +{bonus} проверок."


def register_discount_use(code, user_id):
    """Промокод на скидку: счётчик растёт только когда подписка реально выдана/оплачена."""
    code = (code or "").strip().upper()
    if not code:
        return False, "Пустой код"

    conn = get_connection()
    row = conn.execute("SELECT * FROM promocodes WHERE code = ? AND kind = 'discount'", (code,)).fetchone()
    if not row:
        conn.close()
        return False, "Промокод на скидку не найден"

    if conn.execute("SELECT 1 FROM promo_usage WHERE user_id = ? AND code = ?", (user_id, code)).fetchone():
        conn.close()
        return False, "Этот пользователь уже использовал данный промокод"

    conn.execute("INSERT INTO promo_usage (user_id, code) VALUES (?, ?)", (user_id, code))
    conn.execute("UPDATE promocodes SET used_count = used_count + 1 WHERE code = ?", (code,))
    conn.commit()
    conn.close()
    return True, "Использование скидки засчитано"


def find_discount_promocode(code, tariff, months):
    code = (code or "").strip().upper()
    if not code:
        return False, 0, ""

    conn = get_connection()
    row = conn.execute("SELECT * FROM promocodes WHERE code = ? AND active = 1", (code,)).fetchone()
    conn.close()

    if not row:
        return False, 0, "Промокод не найден"
    if (row["discount_rub"] or 0) <= 0:
        return False, 0, "Этот промокод не даёт скидку в рублях"
    if row["expires_at"] and datetime.fromisoformat(row["expires_at"]) < datetime.now():
        return False, 0, "Срок действия истёк"
    if row["min_tariff"] and row["min_tariff"] != tariff:
        return False, 0, f"Промокод действует только на тариф {row['min_tariff']}"

    return True, int(row["discount_rub"]), ""