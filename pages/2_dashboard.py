import streamlit as st

import config
from core.analyzer import analyze_contract, extract_highlights
from core.contracts import save_analysis, save_contract, spend_checks
from core.file_reader import read_uploaded_file
from core.records import save_highlights
from core.ui import render_header
from database.models import init_db
from utils.auth import get_current_user

init_db()
render_header()

st.title("📄 Загрузка договора")

user = get_current_user()
if not user:
    st.warning("Сначала войди в аккаунт, чтобы анализировать договоры.")
    st.page_link("pages/1_auth.py", label="🔐 Войти / Регистрация")
    st.stop()

st.write(f"Тариф: **{user['tariff']}** · Осталось проверок: **{user['checks_left']}**")

contract_type = st.selectbox("Тип договора", ["Аренда", "Услуги/фриланс", "Трудовой", "NDA", "Кредит", "Другое"])
role = st.selectbox("Твоя роль", ["Арендатор", "Арендодатель", "Исполнитель", "Заказчик", "Работник", "Работодатель", "Другая"])
comment = st.text_area("Что тебя беспокоит? (необязательно)")

source = st.radio("Как загрузить договор", ["Вставить текст", "Загрузить файл (TXT / PDF / DOCX)"])

text = ""
if source == "Вставить текст":
    text = st.text_area("Текст договора", height=300, placeholder="Вставь сюда текст договора...")
else:
    uploaded = st.file_uploader("Выбери файл", type=["txt", "md", "pdf", "docx"])
    if uploaded is not None:
        try:
            text = read_uploaded_file(uploaded)
            if not text.strip():
                st.warning("В этом файле нет текста (возможно, это скан). Распознавание фото появится позже.")
            else:
                st.success(f"Файл прочитан: {len(text)} символов")
        except Exception:
            st.error("Не удалось прочитать файл. Поддерживаются: TXT, MD, PDF с текстом, DOCX.")

if st.button("🚀 Анализировать", type="primary"):
    if not text.strip():
        st.error("Пока пусто — вставь текст или загрузи файл.")
    else:
        cost = 2 if len(text) > config.BIG_DOC_CHARS else 1
        if user["checks_left"] < cost:
            st.error(f"Недостаточно проверок (нужно {cost}). Выбери тариф.")
            st.page_link("pages/4_pricing.py", label="💳 Тарифы")
        else:
            try:
                with st.spinner("AI читает договор..."):
                    report, model = analyze_contract(text, user["tariff"], contract_type, role, comment)
            except Exception:
                st.error("AI сейчас недоступен (или не пополнен баланс API). Проверка НЕ списана — попробуй позже.")
                st.stop()
            spend_checks(user["id"], len(text))
            contract_id = save_contract(user["id"], contract_type, role, text)
            analysis_id = save_analysis(user["id"], contract_id, model, report)
            try:
                with st.spinner("Составляю карту пунктов..."):
                    save_highlights(analysis_id, extract_highlights(text, user["tariff"]))
            except Exception:
                pass
            st.session_state["last_analysis_id"] = analysis_id
            st.success("✅ Анализ готов! Отчёт собран.")
            st.page_link("pages/3_result.py", label="📊 СМОТРЕТЬ ОТЧЁТ", use_container_width=True)