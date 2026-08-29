import streamlit as st

import config
from core.tariffs import TARIFFS
from core.ui import render_header
from database.connection import get_connection
from utils.auth import delete_user, get_current_user, list_users, reset_password_admin

st.set_page_config(page_title="Админ-панель", page_icon="🛠")
render_header()

user = get_current_user()
if not user or user["email"] not in config.ADMIN_EMAILS:
    st.error("Доступ запрещён")
    st.stop()

st.title("🛠 Админ-панель")

users = list_users()

st.subheader("👥 Пользователи")
if not users:
    st.write("Пока никого нет")
    st.stop()

options = {f"#{u['id']} {u['email']} — {u['tariff']} ({u['checks_left']} пров.)": u["id"] for u in users}
label = st.selectbox("Выбрать пользователя", list(options.keys()))
uid = options[label]

c1, c2 = st.columns(2)
with c1:
    new_pass = st.text_input("Временный пароль", value="mca12345")
    if st.button("🔑 Сбросить пароль"):
        reset_password_admin(uid, new_pass)
        st.toast(f"Пароль пользователя #{uid} сброшен", icon="🔑")
with c2:
    st.write("⚠️ Полное удаление")
    if st.button("🗑 Удалить пользователя"):
        delete_user(uid)
        st.toast("Пользователь удалён", icon="🗑")
        st.rerun()

st.divider()
st.subheader("💳 Выдать тариф")
options2 = {u["email"]: u["id"] for u in users}
email2 = st.selectbox("Пользователь", list(options2.keys()), key="grant_email")
tariff = st.selectbox("Тариф", list(TARIFFS.keys()), key="grant_tariff")
if st.button("Выдать", key="grant_btn"):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET tariff = ?, checks_left = ? WHERE id = ?",
        (tariff, TARIFFS[tariff]["checks"], options2[email2]),
    )
    conn.commit()
    conn.close()
    st.toast(f"Тариф {tariff} выдан: {email2}", icon="💳")

st.divider()
st.subheader("🎁 Выдать проверки")
email3 = st.selectbox("Пользователь", list(options2.keys()), key="checks_email")
checks_num = st.number_input("Количество проверок", min_value=0, max_value=100000, value=10, step=1)
mode = st.radio("Как применить", ("Установить ровно", "Добавить к текущим"), horizontal=True)
if st.button("🎁 Выдать проверки", key="checks_btn"):
    conn = get_connection()
    if mode == "Установить ровно":
        conn.execute("UPDATE users SET checks_left = ? WHERE id = ?", (int(checks_num), options2[email3]))
    else:
        conn.execute("UPDATE users SET checks_left = checks_left + ? WHERE id = ?", (int(checks_num), options2[email3]))
    conn.commit()
    conn.close()
    st.toast("Проверки обновлены", icon="🎁")