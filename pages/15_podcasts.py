import streamlit as st

from core.extra_ai import generate_podcast
from core.ui import render_header
from storage.tts import generate_dialogue_audio
from utils.auth import get_current_user

st.set_page_config(page_title="Подкасты", page_icon="🎧")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

st.title("🎧 MCA Подкасты")
st.caption("Персональные аудио-выпуски о юридических ловушках: ИИ пишет и озвучивает двумя голосами.")

TOPICS = [
    "Депозит при аренде квартиры: как не потерять",
    "Трудовой договор: 5 ловушек для новичка",
    "Аренда авто: читаем мелкий шрифт (кейс Делики)",
    "Фриланс: как не остаться без оплаты",
    "Кредитная карусель: скрытые комиссии",
    "NDA: что ты на самом деле подписываешь",
]
topic = st.selectbox("Тема выпуска", TOPICS)

if st.button("🎙 Создать выпуск"):
    with st.spinner("Пишу сценарий и озвучиваю (≈1 минута)..."):
        script = generate_podcast(topic)
        st.session_state["pod_script"] = script
        lines = []
        for raw in script.splitlines():
            raw = raw.strip()
            if raw.upper().startswith("A:"):
                lines.append(("A", raw[2:].strip()))
            elif raw.upper().startswith("B:"):
                lines.append(("B", raw[2:].strip()))
        st.session_state["pod_audio"] = generate_dialogue_audio(lines or [("A", script[:500])])

if st.session_state.get("pod_script"):
    st.subheader("📜 Сценарий")
    st.markdown(st.session_state["pod_script"])
if st.session_state.get("pod_audio"):
    st.subheader("🔊 Слушать")
    st.audio(st.session_state["pod_audio"], format="audio/mpeg")