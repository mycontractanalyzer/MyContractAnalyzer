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

st.title("📚 Загрузчик законов")
st.caption("Открой закон на consultant.ru или pravo.gov.ru, выдели весь текст (Ctrl+A), "
           "скопируй (Ctrl+C) и вставь ниже — сервис сам разобьёт его на статьи.")

prefix = st.text_input("Префикс", "ГК")
title = st.text_input("Название закона", "Гражданский кодекс РФ (часть 1)")
text = st.text_area("Полный текст закона", height=300)

if st.button("📥 Разбить на статьи и сохранить"):
    if text.strip():
        n = ingest_law_text(prefix.strip(), title.strip(), text)
        st.success(f"✅ Сохранено статей: {n}. Теперь анализ будет цитировать их автоматически.")
    else:
        st.warning("Сначала вставь текст закона.")