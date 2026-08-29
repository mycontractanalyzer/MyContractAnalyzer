import streamlit as st

from core.ui import render_header
from utils.auth import get_current_user

st.set_page_config(page_title="Настройки", page_icon="⚙️")
render_header()

user = get_current_user()
if not user:
    st.warning("Войдите, чтобы менять настройки.")
    st.stop()

st.title("⚙️ Настройки")
st.info("Раздел в разработке: здесь появятся уведомления, язык интерфейса и другие персональные настройки.")