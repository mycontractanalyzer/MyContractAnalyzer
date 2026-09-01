import config
from core.analyzer import _parse_json_list
from integrations.deepseek import ask_deepseek
from storage.pack_generator import generate_protocol_docx

PROTOCOL_SYS = """Ты — юрист. Составь протокол разногласий по договору и отчёту.
Верни ТОЛЬКО JSON-массив без markdown:
[{"clause": "номер пункта и суть", "current": "текущая формулировка одним предложением и почему риск", "proposed": "готовая безопасная формулировка"}, ...]
Не более 12 строк, от важного к менее важному. Пункты и суммы — только из текста."""

NOTES_SYS = """Ты — юрист. Клиент получил безопасную редакцию договора (redline).
Кратко объясни главные правки списком:
- **Пункт N:** что изменено → зачем (одно предложение).
5-10 пунктов, простым языком, без воды."""


def generate_protocol(report, contract_text, tariff):
    raw = ask_deepseek(PROTOCOL_SYS,
                       f"ДОГОВОР:\n\n{contract_text[:20000]}\n\nОТЧЁТ:\n\n{report}",
                       config.MODEL_FREE)
    rows = _parse_json_list(raw)
    return [r for r in rows if isinstance(r, dict) and r.get("clause") and r.get("proposed")][:12]


def protocol_docx(rows, email, title):
    return generate_protocol_docx(rows, email, title)


def generate_redline_notes(report, tariff):
    return ask_deepseek(NOTES_SYS, f"ОТЧЁТ О РИСКАХ:\n\n{report[:8000]}", config.MODEL_FREE)