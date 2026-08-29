import secrets

from database.connection import get_connection


def create_company(owner_id, name, max_members=5):
    invite = secrets.token_hex(4).upper()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO companies (name, owner_id, invite_code, max_members) VALUES (?, ?, ?, ?)",
            (name, owner_id, invite, int(max_members)),
        )
        company_id = cur.lastrowid
        conn.execute(
            "INSERT INTO company_members (company_id, user_id, role) VALUES (?, ?, 'owner')",
            (company_id, owner_id),
        )
        conn.execute("UPDATE users SET company_id = ? WHERE id = ?", (company_id, owner_id))
        conn.commit()
    finally:
        conn.close()
    return invite


def get_user_company(user_id):
    conn = get_connection()
    row = conn.execute(
        """SELECT c.*, u.email AS owner_email
           FROM companies c
           JOIN users u ON u.id = c.owner_id
           WHERE c.owner_id = ?""",
        (user_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_member_company(user_id):
    conn = get_connection()
    row = conn.execute(
        """SELECT c.*, cm.role, u.email AS owner_email
           FROM companies c
           JOIN company_members cm ON cm.company_id = c.id
           JOIN users u ON u.id = c.owner_id
           WHERE cm.user_id = ?""",
        (user_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def list_members(company_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT u.id, u.email, cm.role, cm.joined_at
           FROM company_members cm
           JOIN users u ON u.id = cm.user_id
           WHERE cm.company_id = ?""",
        (company_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def join_by_invite(user_id, invite_code):
    code = (invite_code or "").strip().upper()
    if not code:
        return False, "Введите код приглашения"
    conn = get_connection()
    company = conn.execute("SELECT * FROM companies WHERE invite_code = ?", (code,)).fetchone()
    if not company:
        conn.close()
        return False, "Код не найден"
    members = conn.execute(
        "SELECT COUNT(*) c FROM company_members WHERE company_id = ?", (company["id"],)
    ).fetchone()["c"]
    if members >= company["max_members"]:
        conn.close()
        return False, f"В компании уже максимум {company['max_members']} человек"
    if conn.execute(
        "SELECT 1 FROM company_members WHERE user_id = ?", (user_id,)
    ).fetchone():
        conn.close()
        return False, "Вы уже состоите в компании"
    conn.execute(
        "INSERT INTO company_members (company_id, user_id, role) VALUES (?, ?, 'member')",
        (company["id"], user_id),
    )
    conn.execute("UPDATE users SET company_id = ? WHERE id = ?", (company["id"], user_id))
    conn.commit()
    conn.close()
    return True, f"Вы присоединились к компании «{company['name']}»"


def leave_company(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM company_members WHERE user_id = ?", (user_id,))
    conn.execute("UPDATE users SET company_id = NULL WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def company_stats(company_id):
    conn = get_connection()
    members = conn.execute(
        "SELECT user_id FROM company_members WHERE company_id = ?", (company_id,)
    ).fetchall()
    ids = [r["user_id"] for r in members]
    if not ids:
        conn.close()
        return {"members": 0, "analyses": 0, "avg_score": None}
    placeholders = ",".join("?" * len(ids))
    analyses = conn.execute(
        f"SELECT COUNT(*) c FROM analyses WHERE user_id IN ({placeholders})", ids
    ).fetchone()["c"]
    conn.close()
    return {"members": len(ids), "analyses": analyses}