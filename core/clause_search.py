import re

import config
from integrations.deepseek import ask_deepseek


def _norm(q: str) -> str:
    q = (q or "").strip()
    q = re.sub(r"^(пункт|п\.|clause|ст\.|article)\s*", "", q, flags=re.I)
    return q.strip().rstrip(".")


def _pattern(q: str):
    # «5.8» не должно находиться внутри «15.8» или «5.81»
    return re.compile(r"(?<![0-9.])" + re.escape(q) + r"(?![0-9])")


def search_report(report: str, q: str, limit: int = 6):
    q = _norm(q)
    if not q:
        return []
    pat = _pattern(q)
    out = []
    for line in (report or "").splitlines():
        if pat.search(line):
            out.append(line.strip())
            if len(out) >= limit:
                break
    return out


def search_contract(text: str, q: str, limit: int = 4):
    q = _norm(q)
    if not q:
        return []
    pat = _pattern(q)
    out = []
    lines = (text or "").splitlines()
    for i, line in enumerate(lines):
        if pat.search(line):
            block = " ".join(l.strip() for l in lines[i:i + 3] if l.strip())
            out.append(block[:600])
            if len(out) >= limit:
                break
    return out


EXPLAIN_SYS = """Ты — юрист MyContractAnalyzer. Клиент указал пункт договора.
Объясни простым языком: 1) что означает пункт; 2) чем он опасен или безопасен для клиента; 3) что стоит сделать.
Опирайся только на предоставленный текст. Коротко, 3-5 предложений."""


def explain_clause(clause_text: str, report_excerpt: str, tariff: str):
    return ask_deepseek(
        EXPLAIN_SYS,
        f"ПУНКТ ДОГОВОРА:\n\n{clause_text}\n\nФРАГМЕНТ ОТЧЁТА:\n\n{report_excerpt or 'нет'}",
        config.MODEL_FREE,
    )