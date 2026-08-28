import config
from database.connection import get_connection


def save_contract(user_id, contract_type, role, source_text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contracts (user_id, contract_type, role, source_text, char_count) VALUES (?, ?, ?, ?, ?)",
        (user_id, contract_type, role, source_text, len(source_text)),
    )
    conn.commit()
    contract_id = cur.lastrowid
    conn.close()
    return contract_id


def save_analysis(user_id, contract_id, model, report):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO analyses (user_id, contract_id, model, report) VALUES (?, ?, ?, ?)",
        (user_id, contract_id, model, report),
    )
    conn.commit()
    analysis_id = cur.lastrowid
    conn.close()
    return analysis_id


def get_analysis(analysis_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_contract(contract_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def spend_checks(user_id, char_count):
    cost = 2 if char_count > config.BIG_DOC_CHARS else 1
    conn = get_connection()
    row = conn.execute("SELECT checks_left FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None or row["checks_left"] < cost:
        conn.close()
        return False, cost
    conn.execute("UPDATE users SET checks_left = checks_left - ? WHERE id = ?", (cost, user_id))
    conn.commit()
    conn.close()
    return True, cost