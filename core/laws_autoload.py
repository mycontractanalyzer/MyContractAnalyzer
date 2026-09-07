import html
import logging
import re

import requests

from core.laws_loader import ingest_law_text

log = logging.getLogger("mca_laws")

WIKI_API = "https://ru.wikisource.org/w/api.php"
HEADERS = {
    "User-Agent": "MyContractAnalyzer/1.0 (open legal texts loader; contact: support@mycontractanalyzer.ru)"
}

DEFAULT_PACK = [
    ("ГК", "Гражданский кодекс РФ (часть 1)", "Гражданский кодекс Российской Федерации (часть 1)"),
    ("ГК", "Гражданский кодекс РФ (часть 2)", "Гражданский кодекс Российской Федерации (часть 2)"),
    ("ГПК", "Гражданский процессуальный кодекс РФ", "Гражданский процессуальный кодекс Российской Федерации"),
    ("ТК", "Трудовой кодекс РФ", "Трудовой кодекс Российской Федерации"),
    ("ЗоЗПП", "Закон о защите прав потребителей", "Закон РФ о защите прав потребителей"),
    ("152-ФЗ", "Закон о персональных данных", "Федеральный закон о персональных данных"),
    ("40-ФЗ", "Закон об ОСАГО", "Федеральный закон об обязательном страховании гражданской ответственности владельцев транспортных средств"),
    ("СК", "Семейный кодекс РФ", "Семейный кодекс Российской Федерации"),
    ("КоАП", "Кодекс об административных правонарушениях", "Кодекс Российской Федерации об административных правонарушениях"),
    ("АПК", "Арбитражный процессуальный кодекс РФ", "Арбитражный процессуальный кодекс Российской Федерации"),
]


def _search_title(query: str):
    r = requests.get(
        WIKI_API,
        params={"action": "query", "list": "search", "srsearch": query,
                "srlimit": 1, "format": "json"},
        headers=HEADERS, timeout=30)
    r.raise_for_status()
    hits = r.json().get("query", {}).get("search", [])
    return hits[0]["title"] if hits else None


def _fetch_text(title: str):
    r = requests.get(
        WIKI_API,
        params={"action": "parse", "page": title, "prop": "text", "format": "json"},
        headers=HEADERS, timeout=180)
    r.raise_for_status()
    data = r.json()
    if "parse" not in data:
        raise RuntimeError(f"API error: {str(data.get('error', {}))[:200]}")
    raw = data["parse"]["text"]["*"]
    text = re.sub(r"<[^>]+>", "\n", raw)
    return html.unescape(text)


def autoload_law(prefix: str, title: str, search_query: str):
    try:
        found = _search_title(search_query)
        if not found:
            return 0, "не найдено в поиске Викитеки"
        text = _fetch_text(found)
        if not text:
            return 0, "пустой текст страницы"
        n = ingest_law_text(prefix, title, text)
        return n, None
    except Exception as e:
        log.exception("autoload_law failed for %s", title)
        return 0, f"{type(e).__name__}: {str(e)[:150]}"