import logging
import re

import streamlit as st

import config
from core.analyzer import (DEPTH_CONFIG, analyze_contract, analyze_contract_stream,
                           detect_contract_type, extract_highlights,
                           split_report_highlights)
from core.contracts import (list_user_analyses, save_analysis, save_contract,
                            spend_checks)
from core.file_reader import read_uploaded_file
from core.memory import get_memory_context
from core.records import rename_analysis, save_highlights
from core.ui import render_header
from core.vision import ocr_image
from database.models import init_db
from utils.auth import get_current_user

log = logging.getLogger("mca_dashboard")

init_db()
render_header()

st.title("📄 Загрузка договора")

user = get_current_user()
if not user:
    st.warning("Сначала войди в аккаунт, чтобы анализировать договоры.")
    st.page_link("pages/1_auth.py", label="🔐 Войти / Регистрация")
    st.stop()

st.write(f"Тариф: **{user['tariff']}** · Осталось проверок: **{user['checks_left']}**")

# ---------- обработка остановки из прерванного запуска ----------
if st.session_state.get("analysis_running") and st.session_state.get("stop_btn"):
    pct = st.session_state.get("analysis_pct", 0)
    partial = st.session_state.get("partial_report", "") or ""
    st.session_state["analysis_running"] = False
    if pct >= 25 and len(partial.strip()) >= 200:
        ctype = st.session_state.get("analysis_ctype", "Договор")
        spend_checks(user["id"], st.session_state.get("analysis_len", 0))
        contract_id = save_contract(user["id"], ctype,
                                    st.session_state.get("analysis_role", ""),
                                    st.session_state.get("analysis_text", ""))
        analysis_id = save_analysis(
            user["id"], contract_id, st.session_state.get("analysis_model", ""),
            partial + f"\n\n[Отчёт прерван пользователем на {pct}%]")
        rename_analysis(analysis_id, ctype + " (прерван)")
        st.session_state["last_analysis_id"] = analysis_id
        st.warning(f"⏹ Анализ остановлен на {pct}%. Проверка списана, частичный отчёт сохранён.")
        st.page_link("pages/3_result.py", label="📊 Открыть частичный отчёт",
                     use_container_width=True)
    else:
        st.info(f"⏹ Анализ остановлен на {pct}% (меньше 25%) — проверка НЕ списана.")
    st.stop()

# ---------- форма ----------
contract_type = st.selectbox("Тип договора",
                             ["🤖 Авто (AI определит)", "Аренда", "Услуги/фриланс",
                              "Трудовой", "NDA", "Кредит", "Другое"])
jurisdiction = st.selectbox("🌍 Юрисдикция (право страны)",
                            ["Россия", "США", "Германия", "Великобритания",
                             "Казахстан", "ОАЭ", "Другая"])
role = st.selectbox("Твоя роль", ["Арендатор", "Арендодатель", "Исполнитель", "Заказчик",
                                  "Работник", "Работодатель", "Другая"])
comment = st.text_area("Дополнительный комментарий или уточнение запроса (необязательно)")

depth = st.radio(
    "⚙️ Глубина анализа",
    ["⚡ Краткий (5-15 сек)", "⚙️ Стандарт (20-40 сек)", "🔬 Развёрнутый (1-2 мин)"],
    horizontal=True,
)
depth_key = {"⚡ Краткий (5-15 сек)": "brief",
             "⚙️ Стандарт (20-40 сек)": "standard",
             "🔬 Развёрнутый (1-2 мин)": "detailed"}[depth]

source = st.radio("Как загрузить договор",
                  ["Вставить текст", "Загрузить файл (TXT / PDF / DOCX)",
                   "📷 Фото (PNG / JPG / JPEG)"])

text = ""
if source == "Вставить текст":
    text = st.text_area("Текст договора (черновик сохраняется автоматически)", height=300,
                        placeholder="Вставь сюда текст договора...", key="draft_text")
elif source == "Загрузить файл (TXT / PDF / DOCX)":
    uploaded = st.file_uploader("Выбери файл", type=["txt", "md", "pdf", "docx"])
    if uploaded is not None:
        try:
            text = read_uploaded_file(uploaded)
            if not text.strip():
                st.warning("В этом файле нет текста (возможно, это скан). Попробуй «📷 Фото (OCR)».")
            else:
                st.success(f"Файл прочитан: {len(text)} символов")
        except Exception:
            st.error("Не удалось прочитать файл. Поддерживаются: TXT, MD, PDF с текстом, DOCX.")
else:
    photo = st.file_uploader("Выбери фото договора", type=["png", "jpg", "jpeg"])
    if photo is not None:
        with st.spinner("Распознаю текст с фото..."):
            try:
                text = ocr_image(photo.read(), photo.type)
                st.success(f"Текст распознан: {len(text)} символов")
            except Exception:
                st.error("Не удалось распознать фото. Попробуй более чёткий снимок.")

if text.strip():
    lang = "Русский 🇷" if re.search(r"[а-яА-ЯёЁ]", text) else "Английский 🇬🇧"
    st.caption(f"🌐 Язык: {lang} · 📏 Длина: {len(text)} символов")

# ---------- запуск анализа ----------
if st.button("🚀 Анализировать", type="primary"):
    if not text.strip():
        st.error("Пока пусто — вставь текст, загрузи файл или фото.")
    else:
        cost = 2 if len(text) > config.BIG_DOC_CHARS else 1
        if user["checks_left"] < cost:
            st.error(f"Недостаточно проверок (нужно {cost}). Выбери тариф.")
            st.page_link("pages/4_pricing.py", label="💳 Тарифы")
        else:
            ctype = contract_type
            if ctype.startswith("🤖"):
                ctype = detect_contract_type(text)
                st.toast(f"Тип договора: {ctype}", icon="🤖")

            max_tok = DEPTH_CONFIG.get(depth_key, DEPTH_CONFIG["standard"])["max_tokens"]
            st.session_state.update({
                "analysis_running": True,
                "analysis_pct": 0,
                "partial_report": "",
                "analysis_ctype": ctype,
                "analysis_role": role,
                "analysis_text": text,
                "analysis_len": len(text),
                "analysis_model": "",
            })

            bar = st.progress(1, text="Договор анализируется… 0%")
            live = st.empty()
            st.button("⏹ Остановить анализ", key="stop_btn")
            st.caption("Остановка после 25% прогресса — списывается одна проверка "
                       "и сохраняется частичный отчёт. До 25% — проверка не списывается.")

            memory_ctx = get_memory_context(ctype)
            try:
                stream_gen, model = analyze_contract_stream(
                    text, user["tariff"], ctype, role, comment,
                    depth=depth_key, jurisdiction=jurisdiction, memory_ctx=memory_ctx)
                st.session_state["analysis_model"] = model

                chunks = []
                for ch in stream_gen:
                    chunks.append(ch)
                    s = "".join(chunks)
                    pct = min(99, int(len(s) / 2.5 / max_tok * 100))
                    st.session_state["analysis_pct"] = pct
                    st.session_state["partial_report"] = s
                    bar.progress(max(pct, 1), text=f"Договор анализируется… {pct}%")
                    live.markdown(s)

                report = "".join(chunks)
                if len(report.strip()) < 200:
                    report, model = analyze_contract(
                        text, user["tariff"], ctype, role, comment,
                        depth=depth_key, jurisdiction=jurisdiction, memory_ctx=memory_ctx)
                    st.session_state["analysis_model"] = model
                if len(report.strip()) < 200:
                    raise RuntimeError("empty report")

                report, hl_json = split_report_highlights(report)
                bar.progress(100, text="Договор анализируется… 100%")
                live.markdown(report)

                spend_checks(user["id"], len(text))
                contract_id = save_contract(user["id"], ctype, role, text)
                analysis_id = save_analysis(user["id"], contract_id, model, report)
                existing = [(r.get("title") or "") for r in list_user_analyses(user["id"])]
                num = sum(1 for t in existing if t == ctype or t.startswith(ctype + " "))
                rename_analysis(analysis_id, ctype if num == 0 else f"{ctype} {num + 1}")
                if hl_json:
                    save_highlights(analysis_id, hl_json)
                elif depth_key == "detailed":
                    try:
                        save_highlights(analysis_id, extract_highlights(text[:30000], user["tariff"]))
                    except Exception:
                        pass

                st.session_state["analysis_running"] = False
                st.session_state["last_analysis_id"] = analysis_id
                st.session_state["flash_msg"] = "✅ Анализ готов! Отчёт собран."
                st.page_link("pages/3_result.py", label="📊 СМОТРЕТЬ ОТЧЁТ",
                             use_container_width=True)
            except Exception as e:
                log.exception("analysis failed")
                st.session_state["analysis_running"] = False
                bar.empty()
                live.empty()
                st.error(f"AI сейчас недоступен ({type(e).__name__}). Проверка НЕ списана — попробуй позже.")
                st.stop()