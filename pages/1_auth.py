import streamlit as st

from core.ui import render_header
from utils.auth import get_current_user, login_user, register_user

st.set_page_config(page_title="Вход и регистрация", page_icon="🔐")
render_header()

user = get_current_user()

if user:
    st.success(f"Вы вошли как **{user['email']}**")
    st.page_link("pages/5_profile.py", label="👤 Открыть личный кабинет", use_container_width=True)
    st.stop()

st.title("🔐 Вход и регистрация")
st.caption("build 29.08 v6")

tab_login, tab_reg = st.tabs(["Вход", "Регистрация"])

with tab_login:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Пароль", type="password", key="login_pass")
    if st.button("Войти", key="login_btn"):
        ok, msg = login_user(email, password)
        if ok:
            st.success("👋 Успешный вход! Добро пожаловать.")
            st.toast("👋 Успешный вход!", icon="✅")
            st.page_link("pages/5_profile.py", label="👤 Открыть личный кабинет", use_container_width=True)
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
            st.success("🎉 Успешная регистрация!")
            st.toast("🎉 Успешная регистрация!", icon="✅")
        else:
            st.error(msg)
    st.info("После регистрации войдите в аккаунт: вкладка «Вход» → кнопка «Войти».")