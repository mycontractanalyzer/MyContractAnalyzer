import streamlit as st

from core.companies import create_company, get_user_company, leave_company
from core.promocodes import apply_promocode_checks
from core.tariffs import TARIFFS
from core.ui import render_header
from database.connection import get_connection
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

# === БЛОК КОМАНДЫ ДЛЯ BUSINESS ===
if user["tariff"] in ("Business", "Business Pro"):
    st.subheader("🏢 Команда")
    max_members = 20 if user["tariff"] == "Business Pro" else 5
    company = get_user_company(user["id"])
    if not company:
        st.info(f"У вас тариф «{user['tariff']}» — создайте команду до {max_members} человек.")
        new_name = st.text_input("Название компании", placeholder="Например: ООО «Ромашка»")
        if st.button("Создать команду"):
            if not new_name.strip():
                st.error("Укажи название")
            else:
                invite = create_company(user["id"], new_name.strip(), max_members)
                st.success(f"Команда создана! Код приглашения: **{invite}** — отправь его коллегам.")
                st.rerun()
    else:
        st.success(f"Ваша компания: **{company['name']}**")
        st.write(f"Код приглашения для коллег: **{company['invite_code']}**")
        st.caption(f"Максимум участников: {max_members}. Отправь код коллегам — они введут его в своём кабинете.")
        st.page_link("pages/9_company.py", label="🏢 Управление командой", use_container_width=True)

st.divider()

st.subheader("🎟 Промокод на проверки")
st.caption("Скидочные промокоды вводятся при оформлении подписки.")
code_input = st.text_input("Введите промокод", placeholder="Например: START10", key="promo_profile")
if st.button("Активировать промокод"):
    ok, msg = apply_promocode_checks(user["id"], code_input)
    if ok:
        st.success(msg)
        st.rerun()
    else:
        st.error(msg)

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
            st.success(msg)
        else:
            st.error(msg)

st.divider()
st.subheader("🗑 Удаление аккаунта")
st.warning("Это действие необратимо. Все данные будут удалены.")
confirm = st.checkbox("Я понимаю последствия и хочу удалить аккаунт")
if st.button("Удалить аккаунт навсегда", disabled=not confirm):
    delete_user(user["id"])
    logout_user()
    st.success("Аккаунт удалён.")
    st.switch_page("app.py")

st.divider()
if st.button("Выйти из аккаунта"):
    logout_user()
    st.rerun()