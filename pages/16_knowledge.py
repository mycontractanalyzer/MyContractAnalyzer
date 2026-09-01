import streamlit as st

from core.ui import render_header

st.set_page_config(page_title="Библиотека знаний", page_icon="📖")
render_header()

st.title("📖 Библиотека знаний")
st.caption("Реальные разборы ловушек — учись на чужих договорах, а не на своих ошибках.")

st.info("📚 Раздел наполняется. Скоро здесь появятся разборы реальных договоров: автопрокат, аренда, трудовой, кредиты и фриланс.")

st.page_link("pages/2_dashboard.py", label="📄 Проверить свой договор", use_container_width=True)