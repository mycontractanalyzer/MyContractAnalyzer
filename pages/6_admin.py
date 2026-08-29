import streamlit as st

import config
from core.feedback import list_feedbacks
from core.promocodes import create_promocode, deactivate_promocode, list_promocodes
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
tab_users, tab_grant, tab_checks, tab_promo, tab_fb = st.tabs(
    ["👥 Пользователи", "💳 Тариф", "🎁 Проверки", "🎟 Промокоды", "⭐ Отзывы"]
)

with tab_users:
    if not users:
        st.write("Пока никого нет")
    else:
        options = {f"#{u['id']} {u['email']} — {u['tariff']} ({u['checks_left']} пров.)": u["id"] for u in users}
        label = st.selectbox("Выбрать пользователя", list(options.keys()))
        uid = options[label]
        c1, c2 = st.columns(2)
        with c1:
            new_pass = st.text_input("Временный пароль", value="mca12345")
            if st.button("🔑 Сбросить пароль"):
                reset_password_admin(uid, new_pass)
                st.success(f"Пароль сброшен для #{uid}: {new_pass}")
        with c2:
            if st.button("🗑 Удалить пользователя"):
                delete_user(uid)
                st.success("Удалён")
                st.rerun()

with tab_grant:
    if users:
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
            st.success(f"Тариф {tariff} выдан: {email2}")

with tab_checks:
    if users:
        options2 = {u["email"]: u["id"] for u in users}
        email3 = st.selectbox("Пользователь", list(options2.keys()), key="checks_email")
        checks_num = st.number_input("Количество", min_value=0, max_value=100000, value=10, step=1)
        mode = st.radio("Как применить", ("Установить ровно", "Добавить к текущим"), horizontal=True)
        if st.button("🎁 Выдать проверки"):
            conn = get_connection()
            if mode == "Установить ровно":
                conn.execute("UPDATE users SET checks_left = ? WHERE id = ?", (int(checks_num), options2[email3]))
            else:
                conn.execute("UPDATE users SET checks_left = checks_left + ? WHERE id = ?", (int(checks_num), options2[email3]))
            conn.commit()
            conn.close()
            st.success("Готово")

with tab_promo:
    st.subheader("Создать промокод")
    kind = st.selectbox("Тип", ["checks", "discount"], key="promo_kind")
    value = st.number_input("Значение (для checks — количество проверок)", min_value=1, max_value=10000, value=10, step=1)
    if st.button("Создать промокод"):
        code = create_promocode(kind, int(value))
        st.success(f"Создан промокод: **{code}**")

    st.subheader("Активные промокоды")
    promos = list_promocodes()
    if not promos:
        st.write("Пока нет")
    for p in promos:
        c1, c2, c3 = st.columns([3, 2, 1])
        status = "✅ активен" if p["active"] else "❌ выключен"
        c1.write(f"**{p['code']}** — {p['kind']}={p['value']} ({status})")
        c2.write(f"создан: {p['created_at']}")
        if p["active"] and c3.button("Выключить", key=f"off_{p['code']}"):
            deactivate_promocode(p["code"])
            st.rerun()

with tab_fb:
    fbs = list_feedbacks(200)
    if not fbs:
        st.write("Отзывов пока нет")
    else:
        total = len(fbs)
        likes = sum(1 for f in fbs if f["rating"] == 1)
        dislikes = total - likes
        st.write(f"Всего: {total} | 👍 {likes} | 👎 {dislikes} | рейтинг {int(likes/total*100) if total else 0}%")
        for f in fbs:
            emoji = "👍" if f["rating"] == 1 else "👎"
            st.markdown(f"{emoji} **{f['email'] or 'аноним'}** — {f['created_at']}")
            if f["comment"]:
                st.caption(f"💬 {f['comment']}")
            st.divider()