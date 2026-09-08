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
    conn = get_connection()
    _ensure_table(conn)
    cnt = conn.execute("SELECT COUNT(*) AS c FROM laws").fetchone()["c"]
    if cnt == 0:
        try:
            from core.laws_fulltext import FULL_TEXT
            from core.laws_seed import LAWS
        except Exception:
            FULL_TEXT, LAWS = {}, []
        if LAWS:
            conn.executemany(
                "INSERT OR IGNORE INTO laws (code, title, essence, tags, category, full_text) "
                "VALUES (?,?,?,?,?,?)",
                [(c, t, e, tg, cat, FULL_TEXT.get(c, "")) for (c, t, e, tg, cat) in LAWS])
            conn.commit()
    conn.close()


TOPIC_TAGS = {
    "аренд": ["гк", "аренд"], "увол": ["тк", "увольн"], "зарплат": ["тк", "зарплат"],
    "отпуск": ["тк", "отпуск"], "неустойк": ["гк", "неустойк", "пеня"],
    "штраф": ["коап", "штраф"], "ответствен": ["гк", "ответствен"],
    "персональн": ["152-фз", "персональн"], "согласие": ["152-фз", "согласие"],
    "страх": ["40-фз", "осаго", "страхов"], "потребител": ["зозпп", "потребител"],
    "возврат": ["зозпп", "возврат", "предоплат"], "качеств": ["зозпп", "качеств"],
    "подряд": ["гк", "подряд"], "услуг": ["гк", "услуг"], "поставк": ["гк", "поставк"],
    "хранени": ["гк", "хранени"], "заемн": ["тк", "заемн"], "суд": ["гпк", "апк", "подсудност"],
    "претензи": ["гк", "претензи"], "расторж": ["гк", "расторж"],
    "форс-мажор": ["гк", "форс", "непреодолим"], "моральн": ["зозпп", "моральн"],
    "семейн": ["ск", "семейн"], "ребенк": ["ск", "ребенк", "детей"],
    "авторск": ["гк", "авторск"], "исключительн": ["гк", "авторск"],
    "залог": ["гк", "залог"], "имуществ": ["гк", "имуществ"],
    "регистраци": ["гк", "регистраци"], "улучшени": ["гк", "улучшени"],
    "субаренд": ["гк", "субаренд"], "индексац": ["гк", "индексац"],
}


def _extract_keywords(text: str):
    t = (text or "").lower()
    words = [w for w in re.split(r"[^а-яёa-z0-9-]+", t) if len(w) >= 5]
    seen, uniq = set(), []
    for w in words:
        if w not in seen:
            seen.add(w)
            uniq.append(w)
    themes = set()
    for key, tags in TOPIC_TAGS.items():
        if key in t:
            themes.update(tags)
    return uniq[:80], themes


def _best_excerpt(ft: str, words, max_chars: int = 450) -> str:
    ft_low = ft.lower()
    best_pos, best_score = -1, 0
    for m in re.finditer(r"статья\s+\d+[.\d]*", ft_low):
        pos = m.start()
        window = ft_low[pos:pos + 1500]
        score = sum(1 for w in words if w in window)
        if score > best_score:
            best_score = score
            best_pos = pos
        if best_score >= 6:
            break
    if best_pos < 0 or best_score == 0:
        return ft[:max_chars]
    return ft[best_pos:best_pos + max_chars]


def search_laws(query: str, limit: int = 10):
    seed_laws_if_empty()
    words, themes = _extract_keywords(query)
    conn = get_connection()
    rows = conn.execute("SELECT code, title, essence, tags, full_text FROM laws").fetchall()
    conn.close()
    q_low = (query or "").lower()
    stage1 = []
    for r in rows:
        score = 0
        if r["full_text"]:
            score += 5
        tags_low = (r["tags"] or "").lower()
        ti = (r["title"] or "").lower()
        es = (r["essence"] or "").lower()
        for t in themes:
            if t in tags_low:
                score += 6
        for tag in tags_low.split():
            if len(tag) >= 4 and tag in q_low:
                score += 3
        for w in words:
            if w in ti:
                score += 4
            elif w in es:
                score += 2
        if score:
            stage1.append((score, r))
    stage1.sort(key=lambda x: -x[0])
    refined = []
    for score, r in stage1[:40]:
        ft = (r["full_text"] or "").lower()
        if ft:
            hits = sum(1 for w in words if w in ft)
            score += min(10, hits)
        refined.append((score, r))
    refined.sort(key=lambda x: -x[0])
    return [dict(r) for _, r in refined[:limit]]


def laws_context_block(query: str, limit: int = 8, max_chars: int = 450) -> str:
    try:
        items = search_laws(query, limit=limit + 4)
    except Exception:
        return ""
    if not items:
        return ""
    words, _ = _extract_keywords(query)
    with_ft = [i for i in items if (i.get("full_text") or "").strip()]
    only_es = [i for i in items if not (i.get("full_text") or "").strip()]
    lines = []
    for i in with_ft[:6]:
        excerpt = _best_excerpt(i["full_text"].strip(), words, max_chars)
        lines.append(f"- {i['code']} — {i['title']}. ДОСЛОВНО: «{excerpt}»")
    for i in only_es[:3]:
        lines.append(f"- {i['code']} — {i['title']}: {i['essence']}")
    if not lines:
        return ""
    return ("ПРАВОВАЯ БАЗА (нормы РФ):\n" + "\n".join(lines))