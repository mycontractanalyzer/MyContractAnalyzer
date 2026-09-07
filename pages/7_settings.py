import json

import streamlit as st

from core.ui import render_header
from database.connection import get_connection
from utils.auth import change_password, delete_user, get_current_user, logout_user

st.set_page_config(page_title="Настройки", page_icon="⚙️")
render_header()

user = get_current_user()
if not user:
    st.warning("Войдите, чтобы менять настройки.")
    st.stop()

st.title("⚙️ Настройки")

tab_pass, tab_data, tab_danger = st.tabs(["🔑 Пароль", "📦 Мои данные", "🗑 Удаление аккаунта"])

with tab_pass:
    old = st.text_input("Текущий пароль", type="password", key="set_old")
    new = st.text_input("Новый пароль (минимум 6 символов)", type="password", key="set_new")
    new2 = st.text_input("Повторите новый пароль", type="password", key="set_new2")
    if st.button("💾 Сменить пароль", key="set_pass_btn"):
        if new != new2:
            st.error("Новые пароли не совпадают")
        else:
            ok, msg = change_password(user["id"], old, new)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

with tab_data:
    st.write("Скачай все свои данные сервиса (договоры, анализы) одним файлом JSON.")
    if st.button("📥 Сформировать выгрузку", key="set_export"):
        conn = get_connection()
        contracts = [dict(r) for r in conn.execute(
            "SELECT * FROM contracts WHERE user_id = ?", (user["id"],)).fetchall()]
        analyses = [dict(r) for r in conn.execute(
            "SELECT * FROM analyses WHERE user_id = ?", (user["id"],)).fetchall()]
        conn.close()
        payload = json.dumps(
            {"email": user["email"], "contracts": contracts, "analyses": analyses},
            ensure_ascii=False, indent=2, default=str)
        st.download_button("💾 Сохранить файл", payload,
                           file_name="my_mca_data.json", mime="application/json",
                           key="set_download")

with tab_danger:
    st.warning("Аккаунт, все договоры и анализы будут удалены безвозвратно.")
    confirm = st.text_input('Введи слово "УДАЛИТЬ" для подтверждения', key="set_del_confirm")
    if st.button("🗑 Удалить аккаунт", key="set_del_btn"):
        if (confirm or "").strip().upper() in ("УДАЛИТЬ", "DELETE"):
            delete_user(user["id"])
            logout_user()
            st.success("Аккаунт удалён. Жаль, что ты уходишь!")
            st.switch_page("app.py")
        else:
            st.error('Введи слово "УДАЛИТЬ" для подтверждения')