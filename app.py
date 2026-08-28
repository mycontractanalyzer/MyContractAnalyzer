import streamlit as st

from core.i18n import t
from core.pricing_ui import render_pricing
from core.ui import inject_style, render_hero, render_menu
from database.models import init_db

init_db()

st.set_page_config(page_title="MyContractAnalyzer", page_icon="⚖️", layout="wide")

inject_style()
render_hero()
render_menu()

st.write("""
- 🔴 Красные флаги — опасные пункты
- 🟡 Жёлтые флаги — что можно улучшить
- ✅ Чек-лист перед подписанием
""")

st.divider()

col1, col2, col3 = st.columns(3)
col1.header("1. Загрузи договор")
col1.write("Текст, PDF или фото")
col2.header("2. Получи анализ")
col2.write("AI найдёт риски за минуту")
col3.header("3. Подписывай спокойно")
col3.write("Ты знаешь, что подписываешь")

st.divider()

st.markdown(
    "<style>div.stButton > button {padding: 18px 34px !important; font-size: 20px !important;}</style>",
    unsafe_allow_html=True,
)
_, cta_col, _ = st.columns([1, 2, 1])
with cta_col:
    if st.button("Анализировать договор", use_container_width=True):
        st.switch_page("pages/2_dashboard.py")

st.divider()
st.subheader(t("pricing"))
render_pricing()