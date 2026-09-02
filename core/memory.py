import re

from database.connection import get_connection

SCORE_RE = re.compile(r"(?:Риск-скор|Risk score)[^0-9]*(\d{1,3})\s*/\s*100")


def ensure_indexes():
    conn = get_connection()
    conn.execute("CREATE INDEX IF NOT EXISTS idx_analyses_user ON analyses(user_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_contracts_user ON contracts(user_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_feedbacks_user ON feedbacks(user_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_feedbacks_analysis ON feedbacks(analysis_id)")
    conn.commit()
    conn.close()


def get_memory_context(contract_type: str, max_example_len: int = 1500) -> str:
    ensure_indexes()
    conn = get_connection()
    rows = conn.execute(
        """SELECT c.contract_type, a.report
           FROM analyses a JOIN contracts c ON c.id = a.contract_id"""
    ).fetchall()
    feedback = conn.execute(
        "SELECT comment FROM feedbacks WHERE rating <= 2 AND comment != '' "
        "ORDER BY created_at DESC LIMIT 3"
    ).fetchall()
    conn.close()

    parts = []

    scores = {}
    for r in rows:
        m = SCORE_RE.search(r["report"] or "")
        if m:
            scores.setdefault(r["contract_type"] or "Другое", []).append(int(m.group(1)))
    if scores:
        lines = [f"- «{t}»: средний риск-скор {round(sum(v)/len(v))}/100 по {len(v)} анализам."
                 for t, v in scores.items()]
        parts.append("СТАТИСТИКА СЕРВИСА (твоя накопленная норма — не отклоняйся без причины):\n" + "\n".join(lines))

    similar = [r for r in rows if (r["contract_type"] or "Другое") == contract_type]
    if similar:
        excerpt = (similar[-1]["report"] or "")[:max_example_len]
        parts.append(f"ПРИМЕР ПРОШЛОГО АНАЛИЗА по типу «{contract_type}» (согласованность стиля и строгости):\n{excerpt}…")

    notes = [r["comment"] for r in feedback]
    if notes:
        parts.append("УРОКИ ИЗ ЖАЛОБ (не повторяй эти ошибки):\n" + "\n".join(f"- {n}" for n in notes))

    return "\n\n".join(parts)