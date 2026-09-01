import re

import streamlit as st

import config
from core.analyzer import (analyze_contract, detect_contract_type,
                           extract_highlights, smart_compress)
from core.contracts import (list_user_analyses, save_analysis, save_contract,
                            spend_checks)
from core.file_reader import read_uploaded_file
from core.memory import get_memory_context
from core.records import rename_analysis, save_highlights
from core.ui import render_header
from core.vision import ocr_image
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

contract_type = st.selectbox("Тип договора",
                             ["🤖 Авто (AI определит)", "Аренда", "Услуги/фриланс",
                              "Трудовой", "NDA", "Кредит", "Другое"])
jurisdiction = st.selectbox("🌍 Юрисдикция (право страны)",
                            ["Россия", "США", "Германия", "Великобритания",
                             "Казахстан", "ОАЭ", "Другая"])
role = st.selectbox("Твоя роль", ["Арендатор", "Арендодатель", "Исполнитель", "Заказчик",
                                  "Работник", "Работодатель", "Другая"])
comment = st.text_area("Дополнительный комментарий или уточнение запроса (необязательно)")

fmt = st.radio("Формат отчёта", ["📖 Развёрнуто", "📝 Кратко"], horizontal=True)

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
    lang = "Русский 🇷🇺" if re.search(r"[а-яА-ЯёЁ]", text) else "Английский 🇬🇧"
    compressed = smart_compress(text)
    saved = max(0, 100 - int(len(compressed) / max(1, len(text)) * 100))
    st.caption(f"🌐 Язык: {lang} · ✂️ Сжатие экономит ~{saved}% токенов · ⏱ Анализ: ~{15 + min(60, (len(text) // 2000) * 5)} сек")

if st.button("🚀 Анализировать", type="primary"):
    if not text.strip():
        st.error("Пока пусто — вставь текст, загрузи файл или фото.")
    else:
        cost = 2 if len(text) > config.BIG_DOC_CHARS else 1
        if user["checks_left"] < cost:
            st.error(f"Недостаточно проверок (нужно {cost}). Выбери тариф.")
            st.page_link("pages/4_pricing.py", label="💳 Тарифы")
        else:
            est = 15 + min(60, (len(text) // 2000) * 5)
            ctype = contract_type
            try:
                with st.status(f"⏱ Анализирую… осталось примерно {est} сек", expanded=True) as status:
                    if ctype.startswith("🤖"):
                        status.update(label="🤖 Определяю тип договора…")
                        ctype = detect_contract_type(text)
                        st.toast(f"Тип договора: {ctype}", icon="🤖")
                    status.update(label=f"📖 AI читает договор и ищет риски (≈{est} сек)…")
                    memory_ctx = get_memory_context(ctype)
                    report, model = analyze_contract(text, user["tariff"], ctype, role,
                                                     comment, brief=(fmt == "📝 Кратко"),
                                                     jurisdiction=jurisdiction,
                                                     memory_ctx=memory_ctx)
                    status.update(label="💾 Сохраняю отчёт…")
                    spend_checks(user["id"], len(text))
                    contract_id = save_contract(user["id"], ctype, role, text)
                    analysis_id = save_analysis(user["id"], contract_id, model, report)
                    existing = [(r.get("title") or "") for r in list_user_analyses(user["id"])]
                    num = sum(1 for t in existing if t == ctype or t.startswith(ctype + " "))
                    rename_analysis(analysis_id, ctype if num == 0 else f"{ctype} {num + 1}")
                    status.update(label="🗺 Составляю карту пунктов…")
                    try:
                        save_highlights(analysis_id, extract_highlights(text, user["tariff"]))
                    except Exception:
                        pass
                    status.update(label="✅ Анализ готов!", state="complete")
            except Exception:
                st.error("AI сейчас недоступен. Проверка НЕ списана — попробуй позже.")
                st.stop()
            st.session_state["last_analysis_id"] = analysis_id
            st.success("✅ Анализ готов! Отчёт собран.")
            st.page_link("pages/3_result.py", label="📊 СМОТРЕТЬ ОТЧЁТ", use_container_width=True)