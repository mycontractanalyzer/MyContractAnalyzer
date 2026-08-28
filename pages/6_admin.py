import streamlit as st

import config
from core.admin_tools import add_checks, find_user, grant_tariff, list_users
from core.tariffs import TARIFFS
from utils.auth import get_current_user

from core.ui import render_header

render_header()

st.title("🛠️ Админка")

user = get_current_user()
if not user or user["email"] not in config.ADMIN_EMAILS:
    st.error("Доступ запрещён. Только для администратора.")
    st.stop()

st.subheader("🔍 Управление пользователем")
email = st.text_input("Email пользователя")
if st.button("Найти"):
    found = find_user(email)
    if not found:
        st.error("Пользователь не найден")
    else:
        st.success(f"Найден: {found['email']} · тариф {found['tariff']} · проверок {found['checks_left']}")
        st.session_state["admin_target_id"] = found["id"]

if st.session_state.get("admin_target_id"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Добавить 10 проверок"):
            add_checks(st.session_state["admin_target_id"], 10)
            st.success("Готово")
    with col2:
        tariff = st.selectbox("Тариф", list(TARIFFS.keys()))
        months = st.selectbox("Срок", [1, 3, 6, 9, 12, 24])
        if st.button("🎁 Выдать тариф"):
            grant_tariff(st.session_state["admin_target_id"], tariff, months)
            st.success("Тариф выдан")

st.divider()
st.subheader("👥 Все пользователи")
st.dataframe(list_users(), use_container_width=True)