import streamlit as st

from core.extra_ai import lawyer247
from core.records import bump_lawyer_usage, get_lawyer_count
from core.ui import render_header
from storage.tts import generate_audio
from utils.auth import get_current_user

st.set_page_config(page_title="AI-юрист 24/7", page_icon="🤖")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

LIMITS = {"Pro": 20, "Business Pro": 50}

st.title("🤖 AI-юрист 24/7")
st.caption("Безлимитный чат по любым правовым вопросам — не только по твоим договорам.")

if user["tariff"] not in LIMITS:
    st.warning("🔒 AI-юрист 24/7 доступен на тарифах **Pro** и **Business Pro**.")
    st.page_link("app.py", label="💳 Посмотреть тарифы", use_container_width=True)
    st.stop()

limit = LIMITS[user["tariff"]]
used = get_lawyer_count(user["id"])
st.progress(min(1.0, used / limit))
st.caption(f"Использовано сегодня: **{used} / {limit}** запросов")

if "chat247" not in st.session_state:
    st.session_state.chat247 = []

voice = st.checkbox("🔊 Озвучивать ответы")

for q, a in st.session_state.chat247:
    st.markdown(f"**Ты:** {q}")
    st.markdown(f"**Юрист:** {a}")

q = st.text_input("Твой вопрос", placeholder="Например: могут ли уволить во время отпуска?")
if st.button("Спросить"):
    if q.strip():
        ok, cnt = bump_lawyer_usage(user["id"], limit)
        if not ok:
            st.error(f"Лимит на сегодня исчерпан ({limit}). Возвращайся завтра!")
        else:
            with st.spinner("Консультирую..."):
                a = lawyer247(q, user["tariff"])
            st.session_state.chat247.append((q, a))
            if voice:
                st.session_state["audio247"] = generate_audio(a)
            st.rerun()

if st.session_state.get("audio247"):
    st.audio(st.session_state["audio247"], format="audio/mpeg")