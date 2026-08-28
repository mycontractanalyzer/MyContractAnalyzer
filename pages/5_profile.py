import streamlit as st

from core.history import get_user_analyses
from utils.auth import get_current_user, logout_user

from core.ui import render_header
render_header()
st.title("👤 Личный кабинет")

user = get_current_user()
if not user:
    st.warning("Сначала войди в аккаунт")
    st.page_link("pages/1_auth.py", label="🔐 Войти / Регистрация")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Email", user["email"])
c2.metric("Тариф", user["tariff"])
c3.metric("Проверок", user["checks_left"])
c4.metric("Подписка до", user["subscription_end"] or "—")

st.divider()
st.subheader("📚 История анализов")

rows = get_user_analyses(user["id"])
if not rows:
    st.info("Пока нет анализов.")
else:
    for r in rows:
        with st.expander(f"{r['created_at']} · {r['contract_type'] or 'Договор'}"):
            st.markdown(r["report"])

st.divider()
if st.button("🚪 Выйти из аккаунта"):
    logout_user()
    st.rerun()