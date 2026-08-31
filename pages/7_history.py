import streamlit as st

from core.contracts import get_analysis, get_contract, list_user_analyses
from core.ui import render_header
from utils.auth import get_current_user

st.set_page_config(page_title="История проверок", page_icon="📚")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

st.title("📚 История проверок")
st.caption("Открывай прошлые анализы — проверка не списывается.")

rows = list_user_analyses(user["id"])
if not rows:
    st.info("История пока пуста. Загрузи первый договор!")
    st.page_link("pages/2_dashboard.py", label="📄 Загрузить договор")
    st.stop()

for row in rows:
    contract = get_contract(row["contract_id"])
    label = f"📄 {contract['name']} — {row['created_at']} ({row['model']})"
    with st.expander(label):
        st.markdown(row["report"])
        st.page_link(f"pages/3_result.py?aid={row['id']}", label="📊 Открыть отчёт", use_container_width=True)