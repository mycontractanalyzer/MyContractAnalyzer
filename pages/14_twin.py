import streamlit as st

from core.contracts import list_user_analyses
from core.extra_ai import twin_answer
from core.ui import render_header
from utils.auth import get_current_user

st.set_page_config(page_title="Двойник юриста", page_icon="🧠")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

st.title("🧠 Цифровой двойник твоего юриста")
st.caption("ИИ, который знает историю твоих договоров и отвечает в твоём контексте.")

rows = list_user_analyses(user["id"])[:3]
reports = [r["report"][:1500] for r in rows]
if not reports:
    st.info("Двойник станет умнее после первых проверок твоих договоров.")

if "twin_chat" not in st.session_state:
    st.session_state.twin_chat = []

for q, a in st.session_state.twin_chat:
    st.markdown(f"**Ты:** {q}")
    st.markdown(f"**Двойник:** {a}")

q = st.text_input("Вопрос двойнику", placeholder="Например: мне опять прислали похожий договор — что проверить в первую очередь?")
if st.button("Спросить двойника"):
    if q.strip():
        with st.spinner("Думаю в твоём контексте..."):
            a = twin_answer(q, user, reports)
        st.session_state.twin_chat.append((q, a))
        st.rerun()