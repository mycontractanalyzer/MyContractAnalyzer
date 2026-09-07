import json
import re

import requests
import streamlit as st

import config
from core.laws_db import laws_context_block
from core.prompts import (build_benchmark_prompt, build_chat_system_prompt,
                          build_compare_system_prompt, build_highlights_prompt,
                          build_letter_prompt, build_missing_prompt,
                          build_negotiation_prompt, build_passport_prompt,
                          build_redline_prompt, build_system_prompt,
                          build_translate_prompt, build_whatif_prompt)
from integrations.deepseek import ask_deepseek

PAID_TIERS = ("Standard", "Pro", "Business", "Business Pro")

DEPTH_CONFIG = {
    "brief":      {"model_key": "free", "temp": 0.3, "max_tokens": 1500},
    "standard":   {"model_key": "free", "temp": 0.2, "max_tokens": 3500},
    "detailed":   {"model_key": "paid", "temp": 0.2, "max_tokens": 6000},
}

LAWYER247_SYSTEM = (
    "Ты — опытный российский юрист-консультант MyContractAnalyzer. Отвечай по существу, "
    "структурно и понятно для неюриста. При возможности ссылайся на конкретные статьи "
    "законов РФ из предоставленной правовой базы и цитируй их дословно. Если вопрос не "
    "юридический — вежливо откажись. Язык ответа — язык вопроса."
)


def choose_model(tariff: str) -> str:
    return config.MODEL_PAID if tariff in PAID_TIERS else config.MODEL_FREE


def _pick_model_for_depth(tariff: str, depth: str) -> str:
    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["standard"])
    if cfg["model_key"] == "paid" and tariff in PAID_TIERS:
        return config.MODEL_PAID
    return config.MODEL_FREE


def smart_compress(text: str) -> str:
    t = re.sub(r"[ \t]{2,}", " ", text or "")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def _get_api_key():
    return st.secrets.get("DEEPSEEK_API_KEY") or getattr(config, "DEEPSEEK_API_KEY", "")


def _stream_deepseek(system: str, user_msg: str, model: str,
                     max_tokens: int = 3500, temperature: float = 0.2):
    api_key = _get_api_key()
    if not api_key:
        yield "[Ошибка: API ключ DeepSeek не настроен]"
        return

    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        "stream": True,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        with requests.post(url, headers=headers, json=payload, stream=True, timeout=300) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        break
                    try:
                        obj = json.loads(data)
                        delta = obj.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        yield f"\n\n[Ошибка стриминга: {e}]"


def analyze_contract(text, tariff="Free", contract_type="", role="", comment="",
                     depth="standard", jurisdiction="Россия", memory_ctx=""):
    model = _pick_model_for_depth(tariff, depth)
    system = build_system_prompt(tariff, contract_type, role, comment,
                                 brief=(depth == "brief"),
                                 jurisdiction=jurisdiction, memory_ctx=memory_ctx)
    laws_ctx = laws_context_block(text, limit=12)
    if laws_ctx:
        system = system + "\n\n" + laws_ctx
    user_msg = f"Вот текст договора для анализа (режим: {depth}):\n\n{smart_compress(text)}"
    report = ask_deepseek(system, user_msg, model)
    return report, model


def analyze_contract_stream(text, tariff="Free", contract_type="", role="", comment="",
                            depth="standard", jurisdiction="Россия", memory_ctx=""):
    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["standard"])
    model = _pick_model_for_depth(tariff, depth)
    system = build_system_prompt(tariff, contract_type, role, comment,
                                 brief=(depth == "brief"),
                                 jurisdiction=jurisdiction, memory_ctx=memory_ctx)
    laws_ctx = laws_context_block(text, limit=12)
    if laws_ctx:
        system = system + "\n\n" + laws_ctx
    user_msg = f"Вот текст договора для анализа (режим: {depth}):\n\n{smart_compress(text)}"
    gen = _stream_deepseek(system, user_msg, model,
                           max_tokens=cfg["max_tokens"], temperature=cfg["temp"])
    return gen, model


def detect_contract_type(text):
    raw = ask_deepseek(
        "Определи тип договора. Верни ОДНО слово из списка: Аренда, Трудовой, Услуги, NDA, Кредит, Другое. Без пояснений.",
        text[:3000], config.MODEL_FREE)
    low = (raw or "").strip().lower()
    for k in ["аренда", "трудовой", "услуги", "nda", "кредит", "другое"]:
        if k in low:
            return {"nda": "NDA"}.get(k, k.capitalize() if k != "трудовой" else "Трудовой")
    return "Другое"


def generate_passport(text):
    return ask_deepseek(build_passport_prompt(), f"ДОГОВОР:\n\n{text[:20000]}", config.MODEL_FREE)


def generate_missing(text, report, tariff):
    return ask_deepseek(build_missing_prompt(),
                        f"ДОГОВОР:\n\n{text[:20000]}\n\nОТЧЁТ:\n\n{report}", choose_model(tariff))


def translate_contract(text):
    return ask_deepseek(build_translate_prompt(), text[:15000], config.MODEL_FREE)


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
    raw = ask_deepseek(build_highlights_prompt(),
                       f"Текст договора:\n\n{smart_compress(text)[:30000]}", config.MODEL_FREE)
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


def lawyer247_stream(question: str, history: list, tariff: str):
    system = LAWYER247_SYSTEM
    laws_ctx = laws_context_block(question, limit=6)
    if laws_ctx:
        system = system + "\n\n" + laws_ctx
    msgs = []
    for q, a in (history or [])[-5:]:
        msgs.append(f"КЛИЕНТ: {q}")
        msgs.append(f"ЮРИСТ: {a}")
    msgs.append(f"КЛИЕНТ: {question}")
    user_msg = "\n\n".join(msgs)
    model = choose_model(tariff)
    return _stream_deepseek(system, user_msg, model, max_tokens=1200, temperature=0.3), model