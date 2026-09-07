import re

from database.connection import get_connection

ART_RE = re.compile(r"Статья\s+(\d+(?:[.\-]\d+)*)", re.I)


def ingest_law_text(prefix: str, title: str, text: str) -> int:
    conn = get_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS laws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        title TEXT,
        essence TEXT,
        tags TEXT,
        category TEXT,
        full_text TEXT DEFAULT '')""")
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(laws)").fetchall()]
    if "full_text" not in cols:
        conn.execute("ALTER TABLE laws ADD COLUMN full_text TEXT DEFAULT ''")
    parts = ART_RE.split(text)
    added = 0
    it = iter(parts[1:])
    for num, body in zip(it, it):
        body = body.strip()
        if len(body) < 40:
            continue
        code = f"{prefix} {num}"
        head = " ".join(body.split())[:120]
        conn.execute(
            "INSERT OR REPLACE INTO laws (code, title, essence, tags, category, full_text) "
            "VALUES (?,?,?,?,?,?)",
            (code, f"{title} — ст. {num}", head,
             (prefix + " " + title).lower(), "загружено", body[:6000]))
        added += 1
    conn.commit()
    conn.close()
    return added