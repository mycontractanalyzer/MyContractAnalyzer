import html as _html
import json
import re

import streamlit as st

from core.analyzer import (choose_model, generate_benchmark, generate_letter,
                           generate_negotiation, generate_redline, generate_whatif)
from core.contracts import get_analysis, get_contract, list_user_analyses
from core.feedback import save_feedback
from core.prompts import build_chat_system_prompt
from core.records import fmt_dt, rename_analysis, save_consult_request
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

rows = list_user_analyses(user["id"])
if not rows:
    st.info("Пока нет анализа. Загрузи договор.")
    st.page_link("pages/2_dashboard.py", label="📄 Загрузить договор")
    st.stop()

options = {f"{r.get('title') or 'Договор'} · {fmt_dt(r['created_at'])}": r["id"] for r in rows}
labels = list(options.keys())
current = str(st.query_params.get("aid") or st.session_state.get("last_analysis_id") or rows[0]["id"])
default_idx = next((i for i, k in enumerate(labels) if str(options[k]) == current), 0)
sel = st.selectbox("📑 Какой отчёт открыть", labels, index=default_idx)
analysis_id = options[sel]

analysis = get_analysis(analysis_id)
contract = get_contract(analysis["contract_id"])

m = re.search(r"Риск-скор[^0-9]*(\d{1,3})\s*/\s*100", analysis["report"])
if m:
    score = int(m.group(1))
    verdict = ("✅ Можно подписывать" if score <= 30
               else ("🟡 С осторожностью" if score <= 70 else "❌ Не подписывать без правок"))
    st.metric("🎯 Риск-скор договора", f"{score}/100", verdict)

with st.expander("✏️ Переименовать отчёт"):
    cur = analysis.get("title") or (contract.get("contract_type") or "Договор")
    new_title = st.text_input("Название отчёта", value=cur, key="rename_inp")
    if st.button("💾 Сохранить название"):
        rename_analysis(analysis_id, new_title)
        st.success("Сохранено")

with st.expander("📄 Отчёт анализа", expanded=False):
    st.markdown(analysis["report"])

items = []
if analysis.get("highlights"):
    try:
        items = json.loads(analysis["highlights"])
    except Exception:
        items = []

if items:
    with st.expander("🗺 Карта пунктов и подсветка", expanded=False):
        st.caption("Красное — опасные пункты, жёлтое — стоит уточнить.")
        for it in items:
            if it.get("level") == "red":
                st.error(f"**{it.get('quote')}**\n\n{it.get('reason', '')}")
            else:
                st.warning(f"**{it.get('quote')}**\n\n{it.get('reason', '')}")
        escaped = _html.escape(contract["source_text"])
        for it in items:
            q = _html.escape(it.get("quote", ""))
            if q and q in escaped:
                cls = "mca-hl-red" if it.get("level") == "red" else "mca-hl-yellow"
                escaped = escaped.replace(q, f'<mark class="{cls}">{q}</mark>', 1)
        st.markdown(
            "<style>.mca-contract{white-space:pre-wrap;font-size:13px;line-height:1.6;}"
            ".mca-hl-red{background:rgba(255,77,79,.4);color:inherit;padding:0 2px;border-radius:3px;}"
            ".mca-hl-yellow{background:rgba(240,180,41,.4);color:inherit;padding:0 2px;border-radius:3px;}</style>"
            f'<div class="mca-contract">{escaped}</div>',
            unsafe_allow_html=True,
        )

with st.expander("📥 Скачать отчёт", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 Скачать PDF", data=generate_report_pdf(analysis["report"], user["email"]),
                           file_name="MyContractAnalyzer_report.pdf", mime="application/pdf",
                           use_container_width=True)
    with c2:
        st.download_button("📝 Скачать DOCX", data=generate_report_docx(analysis["report"], user["email"]),
                           file_name="MyContractAnalyzer_report.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           use_container_width=True)
    st.page_link("pages/7_history.py", label="📚 История проверок", use_container_width=True)

has_tools = bool(st.session_state.get("nego") or st.session_state.get("whatif") or st.session_state.get("bench"))
with st.expander("🧰 Инструменты переговоров", expanded=has_tools):
    t1, t2, t3 = st.columns(3)
    with t1:
        if st.button("🎙 Скрипт переговоров"):
            with st.spinner("Составляю скрипт..."):
                st.session_state["nego"] = generate_negotiation(
                    contract["source_text"], analysis["report"], user["tariff"])
    with t2:
        scenario = st.selectbox("Сценарий «Что если…»",
                                ["Я просрочу платёж на 2 месяца",
                                 "Контрагент расторгнет договор",
                                 "Я захочу расторгнуть досрочно",
                                 "Своя ситуация..."])
        if scenario == "Своя ситуация...":
            scenario = st.text_input("Опиши ситуацию")
        if st.button("🎭 Что если…"):
            with st.spinner("Моделирую последствия..."):
                st.session_state["whatif"] = generate_whatif(
                    contract["source_text"], analysis["report"], scenario, user["tariff"])
    with t3:
        if st.button("📊 Рыночный эталон"):
            with st.spinner("Сравниваю с рынком..."):
                st.session_state["bench"] = generate_benchmark(
                    contract["source_text"], analysis["report"], user["tariff"])

    if st.session_state.get("nego"):
        st.subheader("🎙 Скрипт переговоров")
        st.markdown(st.session_state["nego"])
    if st.session_state.get("whatif"):
        st.subheader("🎭 Что если…")
        st.markdown(st.session_state["whatif"])
    if st.session_state.get("bench"):
        st.subheader("📊 Рыночный эталон")
        st.markdown(st.session_state["bench"])

has_docs = bool(st.session_state.get("redline") or st.session_state.get("letter"))
with st.expander("📄 Redline и автописьмо", expanded=has_docs):
    rc1, rc2 = st.columns(2)
    with rc1:
        if st.button("📄 Redline-версия (исправленный договор)"):
            with st.spinner("Переписываю опасные пункты..."):
                st.session_state["redline"] = generate_redline(
                    contract["source_text"], analysis["report"], user["tariff"])
    with rc2:
        if st.button("✉️ Автописьмо контрагенту"):
            with st.spinner("Составляю письмо..."):
                st.session_state["letter"] = generate_letter(
                    contract["source_text"], analysis["report"], user["tariff"],
                    contract.get("contract_type", ""), contract.get("role", ""))
    if st.session_state.get("redline"):
        st.download_button("⬇️ Скачать redline (DOCX)",
                           data=generate_report_docx(st.session_state["redline"], user["email"]),
                           file_name="redline_contract.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    if st.session_state.get("letter"):
        st.text_area("Письмо (скопируй или скачай)", value=st.session_state["letter"], height=250)
        st.download_button("⬇️ Скачать письмо (.txt)",
                           data=st.session_state["letter"].encode("utf-8"),
                           file_name="letter_counterparty.txt", mime="text/plain")

with st.expander("🧑‍⚖️ Проконсультироваться с юристом"):
    st.caption("Хочешь, чтобы договор посмотрел живой юрист? Оставь заявку — мы свяжемся.")
    cq = st.text_area("Твой вопрос или что проверить", height=120)
    cc = st.text_input("Telegram или телефон для связи")
    if st.button("Отправить заявку"):
        if not cq.strip():
            st.error("Опиши вопрос")
        else:
            save_consult_request(user["id"], analysis_id, cq, cc)
            st.toast("Заявка отправлена! Мы свяжемся с тобой.", icon="📩")

with st.expander("⭐ Оценить анализ", expanded=True):
    rating = st.selectbox("Оценка от 1 до 5", [5, 4, 3, 2, 1],
                          format_func=lambda x: "⭐" * x)
    fcomment = st.text_input("Комментарий (необязательно)", placeholder="Что можно улучшить?")
    if st.button("Отправить отзыв", key="fb_submit"):
        save_feedback(analysis_id, user["id"], int(rating), fcomment)
        st.toast("Спасибо за оценку!", icon="⭐")

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