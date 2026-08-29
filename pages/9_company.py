import streamlit as st

from core.companies import company_stats, get_user_company
from core.ui import render_header
from database.connection import get_connection
from utils.auth import get_current_user

st.set_page_config(page_title="Команда", page_icon="🏢")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

if user["tariff"] not in ("Business", "Business Pro"):
    st.error("Команда доступна только на тарифах Business и Business Pro.")
    st.stop()

st.title("🏢 Команда")

company = get_user_company(user["id"])
if not company:
    st.info("Вы ещё не создали компанию. Сделайте это в личном кабинете.")
    st.page_link("pages/5_profile.py", label="👤 В личный кабинет")
    st.stop()

st.success(f"**{company['name']}** · владелец: {company['owner_email']}")
st.write(f"Код приглашения для коллег: **{company['invite_code']}**")
st.write(f"Максимум участников: {company['max_members']}")

stats = company_stats(company["id"])
c1, c2 = st.columns(2)
c1.metric("👥 Участников", stats["members"])
c2.metric("🔍 Проведено анализов", stats["analyses"])

st.divider()
st.subheader("Участники и лимиты проверок")

conn = get_connection()
members = conn.execute(
    """SELECT u.id, u.email, u.checks_left, cm.role, cm.joined_at
       FROM company_members cm
       JOIN users u ON u.id = cm.user_id
       WHERE cm.company_id = ?""",
    (company["id"],),
).fetchall()
conn.close()

for m in members:
    badge = "👑 владелец" if m["role"] == "owner" else "👤 участник"
    st.write(f"• **{m['email']}** — {badge} · проверок: **{m['checks_left']}**")
    if m["role"] != "owner":
        kc1, kc2 = st.columns([1, 1])
        with kc1:
            limit = st.number_input(
                "Выдать проверок",
                min_value=0, max_value=100000, value=int(m["checks_left"]), step=1,
                key=f"limit_{m['id']}",
            )
        with kc2:
            if st.button("💾 Установить", key=f"set_{m['id']}"):
                conn = get_connection()
                conn.execute("UPDATE users SET checks_left = ? WHERE id = ?", (int(limit), m["id"]))
                conn.commit()
                conn.close()
                st.toast(f"Лимит для {m['email']} обновлён", icon="💾")
                st.rerun()

st.divider()
st.warning("⚠️ Распустить команду")
st.caption("Удалит компанию и уберёт всех участников. Проверки участников сохранятся.")
if st.button("Распустить команду"):
    conn = get_connection()
    conn.execute("DELETE FROM company_members WHERE company_id = ?", (company["id"],))
    conn.execute("UPDATE users SET company_id = NULL WHERE company_id = ?", (company["id"],))
    conn.execute("DELETE FROM companies WHERE id = ?", (company["id"],))
    conn.commit()
    conn.close()
    st.success("Команда удалена")
    st.rerun()