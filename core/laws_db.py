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


# Ключевые темы → список тегов (для точного поиска)
TOPIC_TAGS = {
    "аренд": ["гк", "аренд", "жилищ"],
    "увол": ["тк", "увольн", "трудов"],
    "зарплат": ["тк", "зарплат", "оплат"],
    "отпуск": ["тк", "отпуск"],
    "неустойк": ["гк", "неустойк", "пеня", "процент"],
    "штраф": ["гк", "коап", "штраф"],
    "ответствен": ["гк", "ответствен"],
    "персональн": ["152-фз", "персональн"],
    "согласие": ["152-фз", "согласие"],
    "страх": ["40-фз", "осаго", "страхов"],
    "потребител": ["зозпп", "потребител"],
    "возврат": ["зозпп", "возврат", "предоплат"],
    "качеств": ["зозпп", "гк", "качеств", "недостатк"],
    "договор": ["гк", "договор"],
    "подряд": ["гк", "подряд"],
    "услуг": ["гк", "услуг"],
    "поставк": ["гк", "поставк"],
    "хранени": ["гк", "хранени"],
    "заемн": ["тк", "заемн"],
    "суд": ["гпк", "апк", "подсудност"],
    "претензи": ["гк", "претензи"],
    "расторж": ["гк", "расторж"],
    "форс-мажор": ["гк", "форс", "непреодолим"],
    "моральн": ["зозпп", "гк", "моральн"],
    "наслед": ["гк", "наслед"],
    "семейн": ["ск", "семейн", "брак", "алимент"],
    "ребенк": ["ск", "ребенк", "детей"],
    "авторск": ["гк", "авторск", "интеллектуальн"],
}


def _extract_keywords(text: str):
    """Вытаскивает ключевые слова и темы из текста договора."""
    t = (text or "").lower()
    words = set(w for w in re.split(r"[^а-яёa-z0-9-]+", t) if len(w) >= 4)
    themes = set()
    for key, tags in TOPIC_TAGS.items():
        if key in t:
            themes.update(tags)
    return words, themes


def search_laws(query: str, limit: int = 12):
    seed_laws_if_empty()
    words, themes = _extract_keywords(query)
    conn = get_connection()
    rows = conn.execute("SELECT code, title, essence, tags, full_text FROM laws").fetchall()
    conn.close()
    scored = []
    for r in rows:
        score = 0
        tags_low = (r["tags"] or "").lower()
        # тематический буст (сильный)
        for t in themes:
            if t in tags_low:
                score += 5
        # тэги
        for tag in (r["tags"] or "").split(","):
            tag = tag.strip().lower()
            if tag and len(tag) >= 4 and tag in (query or "").lower():
                score += 3
        ft = (r["full_text"] or "").lower()
        ti = (r["title"] or "").lower()
        es = (r["essence"] or "").lower()
        for w in words:
            if w in ti:
                score += 4
            elif w in es:
                score += 2
            elif w in ft:
                score += 1
        if score:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return [dict(r) for _, r in scored[:limit]]


def laws_context_block(query: str, limit: int = 12, max_chars: int = 700) -> str:
    items = search_laws(query, limit=limit)
    if not items:
        return ""
    lines = []
    for i in items[:limit]:
        quote = (i.get("full_text") or "").strip()
        if quote:
            if len(quote) > max_chars:
                quote = quote[:max_chars] + "… (приведены ключевые части статьи)"
            lines.append(f"- {i['code']} — {i['title']}. ДОСЛОВНАЯ ФОРМУЛИРОВКА: «{quote}»")
        else:
            lines.append(f"- {i['code']} — {i['title']}: {i['essence']}")
    return ("ПРАВОВАЯ БАЗА (проверенные нормы РФ). ОБЯЗАТЕЛЬНОЕ ПРАВИЛО: "
            "если в анализе упоминаешь статью из этого списка — ПРИВЕДИ её ДОСЛОВНУЮ "
            "формулировку в кавычках и укажи номер (например: «согласно ст. 16 ЗоЗПП: "
            "«...дословная цитата...»»). Если статья не подходит — не выдумывай.\n"
            + "\n".join(lines))