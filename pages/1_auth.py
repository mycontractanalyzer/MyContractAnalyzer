import streamlit as st

from core.ui import render_header
from utils.auth import (get_current_user, get_session_user, login_user, register_user,                           resend_code, save_token_to_device, verify_email)

st.set_page_config(page_title="Вход и регистрация", page_icon="🔐")
render_header()

user = get_current_user()

if user:
    st.switch_page("pages/5_profile.py")

st.title("🔐 Вход и регистрация")

tab_login, tab_reg = st.tabs(["Вход", "Регистрация"])

with tab_login:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Пароль", type="password", key="login_pass")
    remember = st.checkbox("🔒 Запомнить это устройство", value=True, key="remember_chk")
    if st.button("Войти", key="login_btn"):
        ok, msg = login_user(email, password)
        if ok:
            if remember:
                u = get_session_user()
                if u and u.get("token"):
                    save_token_to_device(u["token"])
            st.session_state["flash_msg"] = "👋 Успешный вход! Добро пожаловать."
            st.switch_page("pages/5_profile.py")
        else:
            st.error(msg)
    if st.button("Забыли пароль?", key="forgot_btn"):
        st.info(
            "Автоматическое восстановление пока недоступно. Напишите в поддержку "
            "(Telegram: @MyContractAnalyzerSupport) — администратор сбросит пароль вручную."
        )

with tab_reg:
    pending = st.session_state.get("verify_pending")
    if pending:
        st.subheader("✉️ У меня есть код")
        st.write(f"Мы отправили 6-значный код на **{pending}**. Введите его:")
        code = st.text_input("Код из письма", key="verify_code_input")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Подтвердить", key="verify_btn"):
                ok, msg = verify_email(pending, code)
                if ok:
                    st.session_state.pop("verify_pending", None)
                    from database.connection import get_connection
                    conn = get_connection()
                    row = conn.execute("SELECT id FROM users WHERE email = ?", (pending,)).fetchone()
                    conn.close()
                    if row:
                        st.session_state["user_id"] = row["id"]
                    st.session_state["flash_msg"] = "🎉 Почта подтверждена! Добро пожаловать."
                    st.switch_page("pages/5_profile.py")
                else:
                    st.error(msg)
        with c2:
            if st.button("📮 Отправить код ещё раз", key="resend_btn"):
                ok, msg = resend_code(pending)
                st.info(msg)
        st.divider()

    reg_email = st.text_input("Email", key="reg_email")
    reg_pass = st.text_input("Пароль", type="password", key="reg_pass")
    reg_pass2 = st.text_input("Повторите пароль", key="reg_pass2", type="password")
    if st.button("Создать аккаунт", key="reg_btn"):
        ok, msg = register_user(reg_email, reg_pass, reg_pass2)
        if ok:
            st.session_state["verify_pending"] = (reg_email or "").strip().lower()
            st.info(f"📬 {msg}")
            st.rerun()
        else:
            st.error(msg)
    st.info("Регистрация: создать аккаунт → ввести код из письма → попадёшь в личный кабинет.")