import html
import logging
import re

import requests

from core.laws_loader import ingest_law_text

log = logging.getLogger("mca_laws")

WIKI_API = "https://ru.wikisource.org/w/api.php"
HEADERS = {"User-Agent": "MyContractAnalyzer/1.0 (open legal texts loader; contact: support@mycontractanalyzer.ru)"}

DEFAULT_PACK = [
    ("ГК", "Гражданский кодекс РФ (часть 1)", [
        "Гражданский кодекс Российской Федерации (часть 1)",
        "Гражданский кодекс РФ (часть 1)",
        "Гражданский кодекс часть 1"]),
    ("ГК", "Гражданский кодекс РФ (часть 2)", [
        "Гражданский кодекс Российской Федерации (часть 2)",
        "Гражданский кодекс РФ (часть 2)",
        "Гражданский кодекс часть 2"]),
    ("ГПК", "Гражданский процессуальный кодекс РФ", [
        "Гражданский процессуальный кодекс Российской Федерации",
        "Гражданский процессуальный кодекс РФ"]),
    ("ТК", "Трудовой кодекс РФ", ["Трудовой кодекс Российской Федерации"]),
    ("ЗоЗПП", "Закон о защите прав потребителей", [
        "Закон Российской Федерации о защите прав потребителей",
        "О защите прав потребителей",
        "Закон РФ от 07.02.1992 N 2300-1"]),
    ("152-ФЗ", "Закон о персональных данных", ["Федеральный закон о персональных данных"]),
    ("40-ФЗ", "Закон об ОСАГО", [
        "Федеральный закон об обязательном страховании гражданской ответственности владельцев транспортных средств"]),
    ("СК", "Семейный кодекс РФ", ["Семейный кодекс Российской Федерации"]),
    ("КоАП", "Кодекс об административных правонарушениях", [
        "Кодекс Российской Федерации об административных правонарушениях"]),
    ("АПК", "Арбитражный процессуальный кодекс РФ", [
        "Арбитражный процессуальный кодекс Российской Федерации"]),
]


def _parse_page(title):
    r = requests.get(WIKI_API, params={"action": "parse", "page": title, "prop": "text", "format": "json"},
                     headers=HEADERS, timeout=180)
    r.raise_for_status()
    data = r.json()
    if "parse" not in data:
        return None
    raw = data["parse"]["text"]["*"]
    return html.unescape(re.sub(r"<[^>]+>", "\n", raw))


def _search_titles(query):
    clean = re.sub(r"[()]", " ", query)
    r = requests.get(WIKI_API, params={"action": "query", "list": "search", "srsearch": clean,
                                       "srlimit": 3, "format": "json"}, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return [h["title"] for h in r.json().get("query", {}).get("search", [])]


def autoload_law(prefix, title, candidates):
    try:
        text = None
        for cand in candidates:
            t = _parse_page(cand)
            if t and "Статья" in t:
                text = t
                break
        if not text:
            for cand in candidates:
                for found in _search_titles(cand):
                    t = _parse_page(found)
                    if t and "Статья" in t:
                        text = t
                        break
                if text:
                    break
        if not text:
            return 0, "не найдено в Викитеке"
        n = ingest_law_text(prefix, title, text)
        return n, None
    except Exception as e:
        log.exception("autoload_law failed for %s", title)
        return 0, f"{type(e).__name__}: {str(e)[:150]}"