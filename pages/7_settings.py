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
    "Выберите тему",
    ["Тёмная (как сейчас)" if current == "dark" else "Тёмная",
     "Светлая" if current == "light" else "Светлая"],
    horizontal=True,
)
new_theme = "light" if "Светлая" in choice else "dark"
if new_theme != current:
    conn = get_connection()
    conn.execute("UPDATE users SET theme = ? WHERE id = ?", (new_theme, user["id"]))
    conn.commit()
    conn.close()
    st.success("Тема сохранена. Страница обновится...")
    st.rerun()

st.caption("Светлая тема — для работы днём. Тёмная — для глаз ночью.")

st.divider()
st.subheader("Присоединиться к команде")
st.caption("Если у коллеги тариф Business и он прислал тебе код приглашения — введи его здесь.")
invite = st.text_input("Код приглашения", placeholder="Например: A1B2C3D4")
if st.button("Присоединиться"):
    from core.companies import join_by_invite
    ok, msg = join_by_invite(user["id"], invite)
    if ok:
        st.success(msg)
    else:
        st.error(msg)
    st.rerun()