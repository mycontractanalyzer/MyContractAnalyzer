import json
import re

import config
from core.prompts import (build_benchmark_prompt, build_chat_system_prompt,
                          build_compare_system_prompt, build_highlights_prompt,
                          build_letter_prompt, build_negotiation_prompt,
                          build_redline_prompt, build_system_prompt,
                          build_whatif_prompt)
from integrations.deepseek import ask_deepseek


def choose_model(tariff: str) -> str:
    return config.MODEL_FREE if tariff == "Free" else config.MODEL_PAID


def smart_compress(text: str) -> str:
    """Убирает «воду»: лишние пробелы и пустые строки. Экономит токены, не трогая смысл."""
    t = re.sub(r"[ \t]{2,}", " ", text or "")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def analyze_contract(text, tariff="Free", contract_type="", role="", comment="", brief=False):
    model = choose_model(tariff)
    system = build_system_prompt(tariff, contract_type, role, comment, brief=brief)
    report = ask_deepseek(system, f"Вот текст договора для анализа:\n\n{smart_compress(text)}", model)
    return report, model


def _parse_json_list(raw: str):
    m = re.search(r"\[.*\]", raw or "", re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def extract_highlights(text, tariff="Free"):
    system = build_highlights_prompt()
    raw = ask_deepseek(system, f"Текст договора:\n\n{smart_compress(text)[:30000]}", config.MODEL_FREE)
    items = []
    for it in _parse_json_list(raw)[:10]:
        if isinstance(it, dict) and it.get("quote"):
            items.append({
                "quote": str(it["quote"])[:400],
                "level": "red" if it.get("level") == "red" else "yellow",
                "reason": str(it.get("reason", ""))[:400],
            })
    return json.dumps(items, ensure_ascii=False)


def generate_redline(text, report, tariff):
    return ask_deepseek(build_redline_prompt(),
                        f"ДОГОВОР:\n\n{text}\n\nОТЧЁТ О РИСКАХ:\n\n{report}", choose_model(tariff))


def generate_letter(text, report, tariff, contract_type="", role=""):
    return ask_deepseek(build_letter_prompt(contract_type, role),
                        f"ДОГОВОР:\n\n{text[:20000]}\n\nОТЧЁТ О РИСКАХ:\n\n{report}", choose_model(tariff))


def generate_negotiation(text, report, tariff):
    return ask_deepseek(build_negotiation_prompt(),
                        f"ДОГОВОР:\n\n{text[:20000]}\n\nОТЧЁТ:\n\n{report}", choose_model(tariff))


def generate_whatif(text, report, scenario, tariff):
    return ask_deepseek(build_whatif_prompt(scenario),
                        f"ДОГОВОР:\n\n{text[:20000]}\n\nОТЧЁТ:\n\n{report}", choose_model(tariff))


def generate_benchmark(text, report, tariff):
    return ask_deepseek(build_benchmark_prompt(),
                        f"ДОГОВОР:\n\n{text[:20000]}\n\nОТЧЁТ:\n\n{report}", choose_model(tariff))