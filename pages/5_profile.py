import streamlit as st

from core.ui import render_header
from utils.auth import change_password, delete_user, get_current_user, logout_user

st.set_page_config(page_title="Личный кабинет", page_icon="👤")
render_header()

user = get_current_user()
if not user:
    st.warning("Войдите, чтобы открыть личный кабинет.")
    st.page_link("pages/1_auth.py", label="🔐 Войти")
    st.stop()

st.title("👤 Личный кабинет")
st.write(f"**Email:** {user['email']}")
st.write(f"**Тариф:** {user['tariff']}")
st.write(f"**Осталось проверок:** {user['checks_left']}")
if user["subscription_end"]:
    st.write(f"**Подписка до:** {user['subscription_end']}")

st.divider()
st.subheader("🔑 Сменить пароль")
old_p = st.text_input("Текущий пароль", type="password")
new_p = st.text_input("Новый пароль", type="password")
new_p2 = st.text_input("Повторите новый пароль", type="password")
if st.button("Сменить пароль"):
    if new_p != new_p2:
        st.error("Пароли не совпадают")
    else:
        ok, msg = change_password(user["id"], old_p, new_p)
        if ok:
            st.toast("🔑 Пароль изменён!", icon="✅")
        else:
            st.error(msg)

st.divider()
st.subheader("🗑 Удаление аккаунта")
st.warning(
    "Вы точно хотите удалить ваш аккаунт без возможности восстановления? "
    "Все договоры, анализы, тариф и оставшиеся проверки будут удалены безвозвратно."
)
confirm = st.checkbox("Я понимаю последствия и хочу удалить аккаунт")
if st.button("Удалить аккаунт навсегда", disabled=not confirm):
    delete_user(user["id"])
    logout_user()
    st.toast("Аккаунт удалён. Нам жаль, что вы уходите!", icon="👋")
    st.switch_page("app.py")

st.divider()
if st.button("Выйти из аккаунта"):
    logout_user()
    st.toast("Вы вышли из аккаунта", icon="👋")
    st.rerun()