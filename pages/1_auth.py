import streamlit as st

from database.models import init_db
from utils.auth import get_current_user, login_user, logout_user, register_user

from core.ui import render_header
render_header()
init_db()

st.title("🔐 Вход и регистрация")

user = get_current_user()

if user:
    st.success(f"Вы вошли как: **{user['email']}**")
    st.write(f"Тариф: **{user['tariff']}** · Осталось проверок: **{user['checks_left']}**")
    if st.button("Выйти"):
        logout_user()
        st.rerun()
    st.stop()

tab_login, tab_register = st.tabs(["Вход", "Регистрация"])

with tab_register:
    with st.form("register_form", clear_on_submit=True):
        st.write("Создай аккаунт — 1 бесплатная проверка в подарок")
        reg_email = st.text_input("Email")
        reg_pass = st.text_input("Пароль", type="password")
        reg_pass2 = st.text_input("Повтори пароль", type="password")
        reg_submit = st.form_submit_button("Создать аккаунт", type="primary")

    if reg_submit:
        ok, msg = register_user(reg_email, reg_pass, reg_pass2)
        if ok:
            st.rerun()
        else:
            st.error(msg)

with tab_login:
    with st.form("login_form", clear_on_submit=True):
        log_email = st.text_input("Email")
        log_pass = st.text_input("Пароль", type="password")
        log_submit = st.form_submit_button("Войти", type="primary")

    if log_submit:
        ok, msg = login_user(log_email, log_pass)
        if ok:
            st.rerun()
        else:
            st.error(msg)