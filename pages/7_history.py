import streamlit as st

from core.contracts import get_contract, list_user_analyses
from core.records import fmt_dt
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
    contract = get_contract(row["contract_id"]) or {}
    title = row.get("title") or contract.get("contract_type") or "Договор"
    label = f"📄 {title} — {fmt_dt(row['created_at'])}"
    with st.expander(label):
        st.page_link("pages/3_result.py", label="📊 Открыть отчёт с чатом",
                     query_params={"aid": row["id"]}, use_container_width=True)