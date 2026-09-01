import os

import streamlit as st

from core.ui import render_header
from utils.auth import get_current_user

st.set_page_config(page_title="Подкасты", page_icon="🎧")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

st.title("🎧 MCA Подкасты")
st.caption("Авторские выпуски о юридических ловушках. Новые эпизоды — регулярно!")

POD_DIR = os.path.join(os.path.dirname(__file__), "..", "podcasts")

files = []
if os.path.exists(POD_DIR):
    files = sorted(f for f in os.listdir(POD_DIR) if f.lower().endswith((".mp3", ".m4a", ".wav", ".ogg")))

if not files:
    st.info("🎙 Первые выпуски уже записываются — загляни скоро!")
else:
    for f in files:
        title = os.path.splitext(f)[0].replace("_", " ").replace("-", " ")
        st.markdown(f"**🎙 {title}**")
        st.audio(os.path.join(POD_DIR, f))
        st.divider()