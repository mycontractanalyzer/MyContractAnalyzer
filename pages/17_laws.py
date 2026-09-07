import config
import streamlit as st

from core.laws_loader import ingest_law_text
from core.ui import render_header
from utils.auth import get_session_user

render_header()
user = get_session_user()
if not user or user["email"] not in config.ADMIN_EMAILS:
    st.warning("⛔ Доступ только для администратора.")
    st.stop()

st.title("⚡ Автозагрузка пакета законов")
st.caption("Источник — свободная Викитека (ru.wikisource.org). Тексты законов — общественное "
           "достояние. Редакции могут отставать от актуальных — важное сверяй с pravo.gov.ru.")

if st.button("📦 Загрузить базовый пакет (ГК, ГПК, ТК, ЗоЗПП, 152-ФЗ, 40-ФЗ, СК, КоАП, АПК)"):
    from core.laws_autoload import DEFAULT_PACK, autoload_law
    for prefix, title, query in DEFAULT_PACK:
        with st.status(f"Загружаю: {title}…") as status:
            n = autoload_law(prefix, title, query)
            if n is None:
                status.update(label=f"{title} — ошибка запроса к источнику (см. логи сервера)", state="error")
            elif n:
                status.update(label=f"{title} — статей: {n}", state="complete")
            elif n == 0:
                status.update(label=f"{title} — не найдено в Викитеке", state="error")
    st.success("Готово! Анализ теперь цитирует статьи из полных текстов.")

st.divider()
st.title("📚 Ручная загрузка (для любого другого закона)")
st.caption("Открой закон на consultant.ru или pravo.gov.ru, выдели весь текст (Ctrl+A), "
           "скопируй (Ctrl+C) и вставь ниже — сервис сам разобьёт его на статьи.")

prefix = st.text_input("Префикс", "ГК")
title = st.text_input("Название закона", "Гражданский кодекс РФ (часть 1)")
text = st.text_area("Полный текст закона", height=300)

if st.button("📥 Разбить на статьи и сохранить"):
    if text.strip():
        n = ingest_law_text(prefix.strip(), title.strip(), text)
        st.success(f"✅ Сохранено статей: {n}.")
    else:
        st.warning("Сначала вставь текст закона.")