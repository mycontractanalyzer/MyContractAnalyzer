import streamlit as st

from core.ui import render_header
from database.connection import get_connection
from utils.auth import get_current_user

st.set_page_config(page_title="Настройки", page_icon="⚙️")
render_header()

user = get_current_user()
if not user:
    st.warning("Войдите, чтобы менять настройки.")
    st.stop()

st.title("⚙️ Настройки")

st.subheader("🌗 Тема оформления")
current = user.get("theme") or "dark"
choice = st.radio(
    "Выбери тему",
    ["dark", "light"],
    index=0 if current == "dark" else 1,
    format_func=lambda x: "🌙 Тёмная" if x == "dark" else "☀️ Светлая",
    horizontal=True,
)
if choice != current:
    conn = get_connection()
    conn.execute("UPDATE users SET theme = ? WHERE id = ?", (choice, user["id"]))
    conn.commit()
    conn.close()
    st.success("Тема сохранена!")
    st.rerun()

st.caption("Светлая — для работы днём, тёмная — для глаз ночью.")