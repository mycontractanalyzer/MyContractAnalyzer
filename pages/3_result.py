import re

import streamlit as st

from core.analyzer import choose_model
from core.contracts import get_analysis, get_contract
from core.feedback import save_feedback
from core.prompts import build_chat_system_prompt
from core.ui import render_header
from integrations.deepseek import ask_deepseek
from storage.docx_generator import generate_report_docx
from storage.pdf_generator import generate_report_pdf
from utils.auth import get_current_user

render_header()

st.title("💬 Анализ и чат")

user = get_current_user()
if not user:
    st.warning("Сначала войди в аккаунт.")
    st.stop()

analysis_id = st.session_state.get("last_analysis_id")
if not analysis_id:
    st.info("Пока нет анализа. Загрузи договор.")
    st.page_link("pages/2_dashboard.py", label="📄 Загрузить договор")
    st.stop()

analysis = get_analysis(analysis_id)
contract = get_contract(analysis["contract_id"])

m = re.search(r"Риск-скор[^0-9]*(\d{1,3})\s*/\s*100", analysis["report"])
if m:
    score = int(m.group(1))
    verdict = (
        "✅ Можно подписывать"
        if score <= 30
        else ("🟡 С осторожностью" if score <= 70 else "❌ Не подписывать без правок")
    )
    st.metric("🎯 Риск-скор договора", f"{score}/100", verdict)

st.markdown(analysis["report"])

col1, col2, col3 = st.columns(3)
with col1:
    pdf_bytes = generate_report_pdf(analysis["report"], user["email"])
    st.download_button(
        "📄 Скачать PDF",
        data=pdf_bytes,
        file_name="MyContractAnalyzer_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
with col2:
    docx_bytes = generate_report_docx(analysis["report"], user["email"])
    st.download_button(
        "📝 Скачать Word",
        data=docx_bytes,
        file_name="MyContractAnalyzer_report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
    )
with col3:
    st.page_link("pages/7_history.py", label="📚 История проверок", use_container_width=True)

st.divider()
st.subheader("⭐ Оцените качество анализа")
st.caption("Это поможет нам улучшить сервис.")

rating = st.radio("Оценка", ["👍 Полезно", "👎 Не помогло"], horizontal=True, label_visibility="collapsed")
comment = st.text_input("Комментарий (необязательно)", placeholder="Что можно улучшить?")

if st.button("Отправить отзыв", key="fb_submit"):
    rate = 1 if "Полезно" in rating else -1
    save_feedback(analysis_id, user["id"], rate, comment)
    st.success("Спасибо за отзыв!")

st.divider()
st.subheader("❓ Задай вопрос по договору")

if "chat" not in st.session_state:
    st.session_state.chat = []

for q, a in st.session_state.chat:
    st.markdown(f"**Ты:** {q}")
    st.markdown(f"**Бот:** {a}")

question = st.text_input("Твой вопрос", placeholder="Например: что будет, если просрочу платёж на 3 дня?")
if st.button("Отправить"):
    if question.strip():
        with st.spinner("Думаю..."):
            system = build_chat_system_prompt(contract["source_text"], analysis["report"])
            answer = ask_deepseek(system, question, choose_model(user["tariff"]))
        st.session_state.chat.append((question, answer))
        st.rerun()