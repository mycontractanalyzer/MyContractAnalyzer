import streamlit as st
from datetime import datetime, timedelta

import config
from core.feedback import list_feedbacks
from core.promocodes import create_promocode, deactivate_promocode, list_promocodes
from core.tariffs import DISPLAY_NAMES, TARIFFS
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
    st.subheader("➕ Создать промокод")

    promo_kind = st.radio(
        "Тип промокода",
        ["🎁 На проверки (бонус проверок)", "💰 На скидку (в рублях)"],
        horizontal=True,
    )

    # === Блок: на проверки ===
    if "проверки" in promo_kind:
        checks_bonus = st.number_input(
            "Сколько проверок начислить",
            min_value=1, max_value=10000, value=10, step=1,
            key="p_checks_bonus",
        )
        discount_rub = 0
        min_tariff = None
    # === Блок: на скидку ===
    else:
        discount_rub = st.number_input(
            "Сумма скидки, ₽",
            min_value=1, max_value=100000, value=250, step=50,
            key="p_discount_rub",
        )
        tariff_labels = {"Любой тариф": None, **{DISPLAY_NAMES[t]: t for t in TARIFFS if t != "Free"}}
        min_tariff_label = st.selectbox(
            "На какой тариф действует",
            list(tariff_labels.keys()),
            key="p_min_tariff_label",
        )
        min_tariff = tariff_labels[min_tariff_label]
        checks_bonus = 0

    st.divider()
    st.write("**⏱ Срок действия промокода**")
    dur_mode = st.radio(
        "Длительность",
        ["1 месяц", "3 месяца", "6 месяцев", "9 месяцев", "12 месяцев", "24 месяца", "♾ Неограниченно", "🎯 Точное время"],
        horizontal=False,
        key="p_dur_mode",
    )

    expires_at = None
    now = datetime.now()
    if dur_mode == "1 месяц":
        expires_at = (now + timedelta(days=30)).isoformat(sep=" ", timespec="minutes")
    elif dur_mode == "3 месяца":
        expires_at = (now + timedelta(days=90)).isoformat(sep=" ", timespec="minutes")
    elif dur_mode == "6 месяцев":
        expires_at = (now + timedelta(days=180)).isoformat(sep=" ", timespec="minutes")
    elif dur_mode == "9 месяцев":
        expires_at = (now + timedelta(days=270)).isoformat(sep=" ", timespec="minutes")
    elif dur_mode == "12 месяцев":
        expires_at = (now + timedelta(days=365)).isoformat(sep=" ", timespec="minutes")
    elif dur_mode == "24 месяца":
        expires_at = (now + timedelta(days=730)).isoformat(sep=" ", timespec="minutes")
    elif dur_mode == "♾ Неограниченно":
        expires_at = None
    elif dur_mode == "🎯 Точное время":
        c_y, c_m, c_d, c_h = st.columns(4)
        year = c_y.number_input("Год", min_value=now.year, max_value=now.year + 10, value=now.year + 1, step=1)
        month = c_m.number_input("Месяц", min_value=1, max_value=12, value=now.month, step=1)
        day = c_d.number_input("День", min_value=1, max_value=31, value=now.day, step=1)
        hour = c_h.number_input("Час", min_value=0, max_value=23, value=23, step=1)
        try:
            dt = datetime(int(year), int(month), int(day), int(hour), 0)
            expires_at = dt.isoformat(sep=" ", timespec="minutes")
            st.caption(f"Промокод будет действовать до: **{dt.strftime('%d.%m.%Y %H:%M')}**")
        except ValueError:
            st.warning("Некорректная дата")
            expires_at = None

    st.divider()
    if st.button("🎟 Создать промокод"):
        code = create_promocode(
            kind="checks" if "проверки" in promo_kind else "discount",
            value=checks_bonus if "проверки" in promo_kind else 0,
            discount_rub=discount_rub,
            min_tariff=min_tariff,
            checks_bonus=checks_bonus,
            expires_at=expires_at,
        )
        if expires_at:
            st.success(f"Создан промокод: **{code}** (действует до {expires_at})")
        else:
            st.success(f"Создан промокод: **{code}** (бессрочный)")

    st.divider()
    st.subheader("📋 Все промокоды")
    promos = list_promocodes()
    if not promos:
        st.write("Пока нет")
    for p in promos:
        status = "✅ активен" if p["active"] else "❌ выключен"
        kind_label = "🎁 на проверки" if p["kind"] == "checks" else "💰 на скидку"
        extras = []
        if p["checks_bonus"]:
            extras.append(f"+{p['checks_bonus']} пров.")
        if p["discount_rub"]:
            extras.append(f"−{p['discount_rub']} ₽")
        if p["min_tariff"]:
            extras.append(f"только {DISPLAY_NAMES.get(p['min_tariff'], p['min_tariff'])}")
        if p["expires_at"]:
            extras.append(f"до {p['expires_at']}")
        else:
            extras.append("бессрочно")

        c1, c2, c3 = st.columns([3, 3, 1])
        c1.write(f"**{p['code']}** — {kind_label} ({', '.join(extras)}) [{status}]")
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