import streamlit as st

from core.ui import render_header
from utils.auth import get_current_user, login_user, register_user

st.set_page_config(page_title="Вход и регистрация", page_icon="🔐")
render_header()

user = get_current_user()

if user and st.session_state.pop("go_profile", False):
    st.switch_page("pages/5_profile.py")

if user:
    st.success(f"Вы вошли как **{user['email']}**")
    st.page_link("pages/5_profile.py", label="👤 Перейти в личный кабинет")
    st.stop()

st.title("🔐 Вход и регистрация")
st.caption("build 29.08 v3")

tab_login, tab_reg = st.tabs(["Вход", "Регистрация"])

with tab_login:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Пароль", type="password", key="login_pass")
    if st.button("Войти", key="login_btn"):
        ok, msg = login_user(email, password)
        if ok:
            st.session_state["flash"] = "👋 Добро пожаловать! Вы вошли в аккаунт."
            st.session_state["go_profile"] = True
            st.rerun()
        else:
            st.error(msg)
    if st.button("Забыли пароль?", key="forgot_btn"):
        st.info(
            "Автоматическое восстановление пока недоступно. Напишите в поддержку "
            "(Telegram: @MyContractAnalyzerSupport) — администратор сбросит пароль вручную."
        )

with tab_reg:
    reg_email = st.text_input("Email", key="reg_email")
    reg_pass = st.text_input("Пароль", type="password", key="reg_pass")
    reg_pass2 = st.text_input("Повторите пароль", type="password", key="reg_pass2")
    if st.button("Создать аккаунт", key="reg_btn"):
        ok, msg = register_user(reg_email, reg_pass, reg_pass2)
        if ok:
            st.session_state["flash"] = "🎉 Регистрация успешна! Аккаунт создан, вы вошли автоматически."
            st.session_state["go_profile"] = True
            st.rerun()
        else:
            st.error(msg)