import re

from database.connection import get_connection


def _ensure_table(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS laws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        title TEXT,
        essence TEXT,
        tags TEXT,
        category TEXT)""")
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(laws)").fetchall()]
    if "full_text" not in cols:
        conn.execute("ALTER TABLE laws ADD COLUMN full_text TEXT DEFAULT ''")


def seed_laws_if_empty():
    from core.laws_fulltext import FULL_TEXT
    from core.laws_seed import LAWS
    conn = get_connection()
    _ensure_table(conn)
    cnt = conn.execute("SELECT COUNT(*) AS c FROM laws").fetchone()["c"]
    if cnt == 0:
        conn.executemany(
            "INSERT OR IGNORE INTO laws (code, title, essence, tags, category, full_text) "
            "VALUES (?,?,?,?,?,?)",
            [(c, t, e, tg, cat, FULL_TEXT.get(c, "")) for (c, t, e, tg, cat) in LAWS])
        conn.commit()
    else:
        for code, txt in FULL_TEXT.items():
            conn.execute(
                "UPDATE laws SET full_text = ? WHERE code = ? "
                "AND (full_text IS NULL OR full_text = '')", (txt, code))
        conn.commit()
    conn.close()


def search_laws(query: str, limit: int = 6):
    seed_laws_if_empty()
    q = (query or "").lower()
    words = set(w for w in re.split(r"[^а-яёa-z0-9]+", q) if len(w) >= 5)
    conn = get_connection()
    rows = conn.execute("SELECT code, title, essence, tags, full_text FROM laws").fetchall()
    conn.close()
    scored = []
    for r in rows:
        score = 0
        for tag in (r["tags"] or "").split(","):
            tag = tag.strip()
            if tag and len(tag) >= 4 and tag in q:
                score += 2
        ft = (r["full_text"] or "").lower()
        ti = (r["title"] or "").lower()
        for w in words:
            if w in ti:
                score += 2
            elif w in ft:
                score += 1
        if score:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return [dict(r) for _, r in scored[:limit]]


def laws_context_block(query: str, limit: int = 6, max_chars: int = 900) -> str:
    items = search_laws(query)
    if not items:
        return ""
    lines = []
    for i in items[:limit]:
        quote = (i.get("full_text") or "").strip()
        if quote:
            if len(quote) > max_chars:
                quote = quote[:max_chars] + "… (приведены ключевые части статьи)"
            lines.append(f"- {i['code']} — {i['title']}. Формулировка: «{quote}»")
        else:
            lines.append(f"- {i['code']} — {i['title']}: {i['essence']}")
    return ("ПРАВОВАЯ БАЗА СЕРВИСА (проверенные нормы; при упоминании статьи "
            "цитируй формулировку дословно и указывай её номер):\n" + "\n".join(lines))