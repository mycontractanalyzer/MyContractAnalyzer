import streamlit as st

from core.companies import (get_user_company, list_members,
                             company_stats, leave_company)
from core.ui import render_header
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
st.subheader("Участники")
members = list_members(company["id"])
for m in members:
    badge = "👑 владелец" if m["role"] == "owner" else "👤 участник"
    st.write(f"• **{m['email']}** — {badge} (с {m['joined_at']})")

st.divider()
st.warning("⚠️ Удаление команды")
st.caption("Удалит компанию и уберёт всех участников. Проверки участников сохранятся.")
if st.button("Распустить команду"):
    from database.connection import get_connection
    conn = get_connection()
    conn.execute("DELETE FROM company_members WHERE company_id = ?", (company["id"],))
    conn.execute("UPDATE users SET company_id = NULL WHERE company_id = ?", (company["id"],))
    conn.execute("DELETE FROM companies WHERE id = ?", (company["id"],))
    conn.commit()
    conn.close()
    st.success("Команда удалена")
    st.rerun()