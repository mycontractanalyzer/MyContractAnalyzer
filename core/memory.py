import re

from database.connection import get_connection

SCORE_RE = re.compile(r"Риск-скор[^0-9]*(\d{1,3})\s*/\s*100")


def get_memory_context(contract_type: str, max_example_len: int = 1200) -> str:
    """Память сервиса: статистика, пример прошлого анализа, жалобы из отзывов."""
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

    # 1. Статистика по типам договоров
    scores = {}
    for r in rows:
        m = SCORE_RE.search(r["report"] or "")
        if m:
            scores.setdefault(r["contract_type"] or "Другое", []).append(int(m.group(1)))
    if scores:
        lines = [f"- «{t}»: средний риск-скор {round(sum(v)/len(v))}/100 по {len(v)} анализам."
                 for t, v in scores.items()]
        parts.append("СТАТИСТИКА СЕРВИСА (это твоя накопленная норма — сравнивай с ней "
                     "и не отклоняйся без веской причины):\n" + "\n".join(lines))

    # 2. Пример прошлого анализа того же типа (согласованность стиля и строгости)
    similar = [r for r in rows if (r["contract_type"] or "Другое") == contract_type]
    if similar:
        excerpt = (similar[-1]["report"] or "")[:max_example_len]
        parts.append(f"ПРИМЕР ТВОЕГО ПРОШЛОГО АНАЛИЗА по типу «{contract_type}» "
                     f"(сохраняй согласованность стиля и строгости):\n{excerpt}…")

    # 3. Жалобы пользователей (обучение на ошибках)
    notes = [r["comment"] for r in feedback]
    if notes:
        parts.append("ПРОШЛЫЕ ЖАЛОБЫ ПОЛЬЗОВАТЕЛЕЙ (не повторяй эти ошибки):\n"
                     + "\n".join(f"- {n}" for n in notes))

    return "\n\n".join(parts)