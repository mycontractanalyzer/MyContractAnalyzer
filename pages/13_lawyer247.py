import streamlit as st

from core.extra_ai import lawyer247
from core.ui import render_header
from storage.tts import generate_audio
from utils.auth import get_current_user

st.set_page_config(page_title="AI-юрист 24/7", page_icon="🤖")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

st.title("🤖 AI-юрист 24/7")
st.caption("Безлимитный чат по любым правовым вопросам — не только по твоим договорам.")

if "chat247" not in st.session_state:
    st.session_state.chat247 = []

voice = st.checkbox("🔊 Озвучивать ответы")

for q, a in st.session_state.chat247:
    st.markdown(f"**Ты:** {q}")
    st.markdown(f"**Юрист:** {a}")

q = st.text_input("Твой вопрос", placeholder="Например: могут ли уволить во время отпуска?")
if st.button("Спросить"):
    if q.strip():
        with st.spinner("Консультирую..."):
            a = lawyer247(q, user["tariff"])
        st.session_state.chat247.append((q, a))
        if voice:
            st.session_state["audio247"] = generate_audio(a)
        st.rerun()

if st.session_state.get("audio247"):
    st.audio(st.session_state["audio247"], format="audio/mpeg")