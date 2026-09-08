import streamlit as st

from core.ui import render_header
from database.connection import get_connection
from utils.auth import get_current_user

st.set_page_config(page_title="Поддержка", page_icon="💬")
render_header()

st.title("💬 Поддержка")
st.caption("Отвечаем обычно в течение часа, ежедневно с 9:00 до 21:00 (МСК).")

conn = get_connection()
conn.execute("""CREATE TABLE IF NOT EXISTS support_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT, topic TEXT, message TEXT,
    replied INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')))""")
conn.commit()
conn.close()

user = get_current_user()
email = st.text_input("Твой email", value=(user or {}).get("email", ""))
topic = st.selectbox("Тема", ["Вопрос по анализу", "Оплата и тарифы", "Техническая проблема", "Предложение", "Другое"])
msg = st.text_area("Сообщение", height=160)

if st.button("📨 Отправить"):
    if email.strip() and msg.strip():
        conn = get_connection()
        conn.execute("INSERT INTO support_messages (email, topic, message) VALUES (?,?,?)",
                     (email.strip(), topic, msg.strip()))
        conn.commit()
        conn.close()
        st.success("✅ Сообщение получено! Ответим на email и в Telegram.")
    else:
        st.warning("Заполни email и сообщение.")

with st.expander("❓ Частые вопросы"):
    st.markdown("""
**Как получить отчёт?** Раздел «Анализ договора» → загрузи файл → отчёт появится на экране и придёт на почту.
**Не пришёл код подтверждения?** Проверь «Спам» и напиши нам — подтвердим вручную.
**Как удалить свои данные?** Напиши в поддержку — удалим в течение 24 часов.
""")