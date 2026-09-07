import html
import logging
import re

import requests

from core.laws_loader import ingest_law_text

log = logging.getLogger("mca_laws")

WIKI_API = "https://ru.wikisource.org/w/api.php"
UA = {"User-Agent": "MyContractAnalyzer/1.0 (open legal texts loader; contact: support@mycontractanalyzer.ru)"}

# Кандидаты теперь с правильными именами страниц (по разведданным)
DEFAULT_PACK = [
    ("ГК", "Гражданский кодекс РФ (часть 1)", [
        "Гражданский кодекс РФ/Часть первая",
        "Гражданский кодекс РФ часть первая",
    ]),
    ("ГК", "Гражданский кодекс РФ (часть 2)", [
        "Гражданский кодекс РФ/Часть вторая",
    ]),
    ("ГПК", "Гражданский процессуальный кодекс РФ", [
        # ГПК разбит на главы — особая обработка ниже
    ]),
    ("ТК", "Трудовой кодекс РФ", ["Трудовой кодекс Российской Федерации"]),
    ("ЗоЗПП", "Закон о защите прав потребителей", [
        "Закон РФ от 07.02.1992 № 2300-I",
        "Закон РФ от 07.02.1992 № 2300-1",
    ]),
    ("152-ФЗ", "Закон о персональных данных", ["Федеральный закон о персональных данных"]),
    ("40-ФЗ", "Закон об ОСАГО", [
        "Федеральный закон об обязательном страховании гражданской ответственности владельцев транспортных средств"]),
    ("СК", "Семейный кодекс РФ", ["Семейный кодекс Российской Федерации"]),
    ("КоАП", "Кодекс об административных правонарушениях", [
        "Кодекс Российской Федерации об административных правонарушениях"]),
    ("АПК", "Арбитражный процессуальный кодекс РФ", [
        "Арбитражный процессуальный кодекс Российской Федерации"]),
]

# Запасные ссылки на pravo.gov.ru (официальный источник, по номерам документов)
PRAVO_FALLBACK = {
    "Закон РФ от 07.02.1992 № 2300-I": "http://pravo.gov.ru/proxy/ips/?docbody=&nd=102007887",
    "Гражданский кодекс РФ/Часть первая": "http://pravo.gov.ru/proxy/ips/?docbody=&nd=102001614",
    "Гражданский процессуальный кодекс РФ": "http://pravo.gov.ru/proxy/ips/?docbody=&nd=102028801",
}


def _wiki_parse(title):
    r = requests.get(WIKI_API, params={"action": "parse", "page": title, "prop": "text", "format": "json"},
                     headers=UA, timeout=180)
    r.raise_for_status()
    data = r.json()
    if "parse" not in data:
        return None
    raw = data["parse"]["text"]["*"]
    return html.unescape(re.sub(r"<[^>]+>", "\n", raw))


def _wiki_search_titles(query):
    r = requests.get(WIKI_API, params={"action": "query", "list": "search", "srsearch": query,
                                       "srlimit": 3, "format": "json"}, headers=UA, timeout=30)
    r.raise_for_status()
    return [h["title"] for h in r.json().get("query", {}).get("search", [])]


def _load_gpk():
    """ГПК разбит на главы — собираем текст со всех подстраниц."""
    full = []
    for ch in range(1, 50):
        title = f"Гражданский процессуальный кодекс РФ/Глава {ch}"
        try:
            t = _wiki_parse(title)
            if t and "Статья" in t:
                full.append(t)
        except Exception:
            continue
    return "\n\n".join(full) if full else None


def _try_pravo(page_name):
    """Запасной источник: pravo.gov.ru (официальный)."""
    url = PRAVO_FALLBACK.get(page_name)
    if not url:
        return None
    try:
        r = requests.get(url, headers=UA, timeout=60)
        r.raise_for_status()
        # pravo.gov.ru возвращает HTML — выдираем текст
        text = html.unescape(re.sub(r"<[^>]+>", "\n", r.text))
        if "Статья" in text and len(text) > 5000:
            return text
    except Exception as e:
        log.exception("pravo.gov.ru fallback failed for %s: %s", page_name, e)
    return None


def autoload_law(prefix, title, candidates):
    try:
        text = None
        source = "не найден"
        # 1) Особый случай для ГПК — главы
        if prefix == "ГПК":
            text = _load_gpk()
            if text:
                source = "wikisource (главы)"
        # 2) Обычные кандидаты Викитеки
        if not text:
            for cand in candidates:
                try:
                    t = _wiki_parse(cand)
                except Exception:
                    t = None
                if t and "Статья" in t:
                    text = t
                    source = "wikisource"
                    break
            if not text:
                for cand in candidates:
                    for found in _wiki_search_titles(cand):
                        try:
                            t = _wiki_parse(found)
                        except Exception:
                            t = None
                        if t and "Статья" in t:
                            text = t
                            source = "wikisource (search)"
                            break
                    if text:
                        break
        # 3) Fallback: pravo.gov.ru
        if not text:
            for cand in candidates:
                t = _try_pravo(cand)
                if t:
                    text = t
                    source = "pravo.gov.ru"
                    break
        if not text:
            return 0, "не найдено ни в Викитеке, ни на pravo.gov.ru"
        n = ingest_law_text(prefix, title, text)
        return n, None, source
    except Exception as e:
        log.exception("autoload_law failed for %s", title)
        return 0, f"{type(e).__name__}: {str(e)[:150]}", "error"