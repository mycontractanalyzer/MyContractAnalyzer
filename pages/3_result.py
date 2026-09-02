import html as _html
import json
import re

import streamlit as st

from core.analyzer import (choose_model, generate_benchmark, generate_letter,
                           generate_missing, generate_negotiation, generate_passport,
                           generate_redline, generate_whatif, translate_contract)
from core.contracts import get_analysis, get_contract, list_user_analyses
from core.extra_ai import generate_precedent
from core.feedback import get_feedback, upsert_feedback
from core.mailer import send_report_email
from core.clause_search import explain_clause, search_contract, search_report
from core.prompts import build_chat_system_prompt
from core.protocol import generate_protocol, generate_redline_notes, protocol_docx
from core.records import (fmt_dt, rename_analysis, save_checklist,
                          save_consult_request, set_share)
from core.ui import render_header
from integrations.deepseek import ask_deepseek
from storage.docx_generator import generate_report_docx
from storage.pack_generator import generate_lawyer_pack
from storage.pdf_generator import generate_report_pdf
from storage.tts_clean import generate_audio
from utils.auth import get_current_user

render_header()

st.title("💬 Анализ и чат")

user = get_current_user()
aid_q = st.query_params.get("aid")

if not user:
    if aid_q:
        guest = get_analysis(aid_q)
        if guest and guest.get("share"):
            st.title("📄 Отчёт (общий доступ)")
            st.markdown(guest["report"])
            st.caption("Сгенерировано MyContractAnalyzer · See what you're signing")
            st.stop()
    st.warning("Сначала войди в аккаунт.")
    st.stop()

rows = list_user_analyses(user["id"])
if not rows:
    st.info("Пока нет анализа. Загрузи договор.")
    st.page_link("pages/2_dashboard.py", label="📄 Загрузить договор")
    st.stop()

options = {f"{r.get('title') or 'Договор'} · {fmt_dt(r['created_at'])}": r["id"] for r in rows}
labels = list(options.keys())
current = str(aid_q or st.session_state.get("last_analysis_id") or rows[0]["id"])
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

with st.expander("✏️ Переименовать / поделиться"):
    cur = analysis.get("title") or (contract.get("contract_type") or "Договор")
    new_title = st.text_input("Название отчёта", value=cur, key="rename_inp")
    if st.button("💾 Сохранить название"):
        rename_analysis(analysis_id, new_title)
        st.success("Сохранено")
    if st.button("🔗 Поделиться отчётом по ссылке"):
        set_share(analysis_id, 1)
        st.code(f"https://mycontractanalyzer.streamlit.app/3_result?aid={analysis_id}")
        st.caption("Скопируй ссылку — любой человек сможет прочитать отчёт.")

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

cm = re.search(r"Чек-лист:?\*?\s*\n(.*?)(\n###|\n📌|\Z)", analysis["report"], re.S)
cl_items = [l[2:].replace("**", "").strip() for l in (cm.group(1).splitlines() if cm else [])
            if l.strip().startswith("- ")]
if cl_items:
    done = []
    if analysis.get("checklist"):
        try:
            done = json.loads(analysis["checklist"])
        except Exception:
            done = []
    done = (done + [False] * len(cl_items))[:len(cl_items)]
    with st.expander(f"✅ Чек-лист перед подписанием ({sum(done)}/{len(cl_items)})", expanded=False):
        new_done = []
        for i, item in enumerate(cl_items):
            new_done.append(st.checkbox(item, value=done[i], key=f"cl_{i}"))
        if new_done != done and st.button("💾 Сохранить прогресс чек-листа"):
            save_checklist(analysis_id, json.dumps(new_done, ensure_ascii=False))
            st.success("Прогресс сохранён")

with st.expander("📥 Скачать / послушать / отправить", expanded=False):
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
    st.download_button(
        "📤 Пакет для юриста (отчёт + договор, DOCX)",
        data=generate_lawyer_pack(analysis["report"], contract["source_text"], user["email"],
                                  analysis.get("title") or "Договор"),
        file_name="lawyer_pack.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True)
    st.text_area(
        "Письмо юристу (скопируй и приложи пакет)",
        value=f"Здравствуйте!\n\nПрошу проверить договор «{analysis.get('title') or 'Договор'}» и приложенный отчёт ИИ-аналитика. Интересует заключение по рискам, доработка спорных пунктов и стоимость работы.\n\nС уважением, {user['email']}",
        height=140)
    if st.button("🧾 Протокол разногласий (таблица DOCX)"):
        with st.spinner("Готовлю протокол..."):
            st.session_state["proto_rows"] = generate_protocol(
                analysis["report"], contract["source_text"], user["tariff"])
    if st.session_state.get("proto_rows"):
        st.download_button(
            "⬇️ Скачать протокол разногласий (DOCX)",
            data=protocol_docx(st.session_state["proto_rows"], user["email"],
                               analysis.get("title") or "Договор"),
            file_name="protocol_raznoglasiy.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    if st.button("📧 Отправить отчёт на почту"):
        try:
            pdf = generate_report_pdf(analysis["report"], user["email"])
            if send_report_email(user["email"], pdf, analysis.get("title") or "Договор"):
                st.toast(f"Отчёт отправлен на {user['email']}", icon="📧")
            else:
                st.error("Почта не настроена: добавь GMAIL_EMAIL и GMAIL_APP_PASSWORD в Secrets.")
        except Exception:
            st.error("Не удалось отправить. Проверь секреты и попробуй ещё раз.")
    if st.button("🔊 Аудиоверсия отчёта"):
        with st.spinner("Озвучиваю отчёт..."):
            st.session_state["audio_v3"] = generate_audio(analysis["report"])
    if st.session_state.get("audio_v3"):
        st.audio(st.session_state["audio_v3"], format="audio/mpeg")
    st.page_link("pages/7_history.py", label="📚 История проверок", use_container_width=True)

has_tools = bool(st.session_state.get(k) for k in
                 ("nego", "whatif", "bench", "passport", "missing", "translate", "precedent"))
with st.expander("🧰 Инструменты", expanded=has_tools):
    t1, t2, t3 = st.columns(3)
    with t1:
        if st.button("🎙 Скрипт переговоров"):
            with st.spinner("Составляю скрипт..."):
                st.session_state["nego"] = generate_negotiation(
                    contract["source_text"], analysis["report"], user["tariff"])
        if st.button("🪪 Паспорт договора"):
            with st.spinner("Составляю паспорт..."):
                st.session_state["passport"] = generate_passport(contract["source_text"])
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
        if st.button("🕳 Чего не хватает в договоре"):
            with st.spinner("Ищу отсутствующие пункты..."):
                st.session_state["missing"] = generate_missing(
                    contract["source_text"], analysis["report"], user["tariff"])
    with t3:
        if st.button("📊 Рыночный эталон"):
            with st.spinner("Сравниваю с рынком..."):
                st.session_state["bench"] = generate_benchmark(
                    contract["source_text"], analysis["report"], user["tariff"])
        if st.button("🌐 Перевести договор (RU↔EN)"):
            with st.spinner("Перевожу..."):
                st.session_state["translate"] = translate_contract(contract["source_text"])
        if st.button("⚖️ Прецедент-радар"):
            with st.spinner("Ищу судебную практику..."):
                st.session_state["precedent"] = generate_precedent(
                    contract["source_text"], analysis["report"], user["tariff"])

    for key, head in [("passport", "🪪 Паспорт договора"), ("missing", "🕳 Чего не хватает"),
                      ("nego", "🎙 Скрипт переговоров"), ("whatif", "🎭 Что если…"),
                      ("bench", "📊 Рыночный эталон"), ("translate", "🌐 Перевод договора"),
                      ("precedent", "⚖️ Прецедент-радар")]:
        if st.session_state.get(key):
            st.subheader(head)
            st.markdown(st.session_state[key])

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
        if st.button("💬 Почему такие правки"):
            with st.spinner("Объясняю..."):
                st.session_state["redline_notes"] = generate_redline_notes(
                    analysis["report"], user["tariff"])
        if st.session_state.get("redline_notes"):
            st.markdown(st.session_state["redline_notes"])
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

with st.expander("🔍 Поиск по пункту: введи номер — получи разбор", expanded=False):
    q = st.text_input("Номер пункта", placeholder="Например: 5.8 или 4.j")
    if q.strip():
        rep_hits = search_report(analysis["report"], q)
        con_hits = search_contract(contract["source_text"], q)
        if not rep_hits and not con_hits:
            st.info("Не нашёл упоминаний этого пункта в отчёте и договоре.")
        else:
            if con_hits:
                st.markdown("**Пункт в договоре:**")
                for h in con_hits:
                    st.markdown(f"> {h}")
            if rep_hits:
                st.markdown("**Что говорит отчёт:**")
                for h in rep_hits:
                    st.markdown(h)
            if st.button("🧠 Объясни этот пункт простыми словами"):
                with st.spinner("Объясняю..."):
                    st.session_state["clause_explain"] = explain_clause(
                        "\n".join(con_hits) or q, "\n".join(rep_hits), user["tariff"])
            if st.session_state.get("clause_explain"):
                st.success(st.session_state["clause_explain"])

with st.expander("⭐ Оценить анализ (1 отзыв на договор, можно изменить)", expanded=True):
    existing = get_feedback(user["id"], analysis_id)
    rating = st.selectbox("Оценка от 1 до 5", [5, 4, 3, 2, 1],
                          index=[5, 4, 3, 2, 1].index(existing["rating"]) if existing else 0,
                          format_func=lambda x: "⭐" * x)
    fcomment = st.text_input("Комментарий (необязательно)",
                             value=existing["comment"] if existing else "",
                             placeholder="Что можно улучшить?")
    if st.button("Отправить / обновить отзыв", key="fb_submit"):
        upsert_feedback(analysis_id, user["id"], int(rating), fcomment)
        st.toast("Отзыв сохранён! Спасибо.", icon="⭐")

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