import streamlit as st

import config
from core.mailer import _send
from core.ui import render_header
from database.connection import get_connection
from utils.auth import get_session_user

render_header()
user = get_session_user()
if not user or user["email"] not in config.ADMIN_EMAILS:
    st.warning("⛔ Доступ только для администратора.")
    st.stop()

st.title("📨 Поддержка (обращения)")
st.caption("Здесь видны все сообщения с формы поддержки. Ответ уйдёт пользователю на email.")

conn = get_connection()
conn.execute("""CREATE TABLE IF NOT EXISTS support_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT, topic TEXT, message TEXT,
    replied INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')))""")
cols = [r["name"] for r in conn.execute("PRAGMA table_info(support_messages)").fetchall()]
if "replied" not in cols:
    conn.execute("ALTER TABLE support_messages ADD COLUMN replied INTEGER DEFAULT 0")
    conn.commit()
rows = conn.execute("SELECT * FROM support_messages ORDER BY id DESC").fetchall()
conn.close()

if not rows:
    st.info("Пока обращений нет.")
    st.stop()

for r in rows:
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"**{r['email']}** · {r['topic']} · {r['created_at']}")
            st.write(r["message"])
        with c2:
            st.markdown("✅ Отвечено" if r["replied"] else "🔴 Новое")
        with st.expander("✍️ Ответить"):
            answer = st.text_area("Текст ответа", key=f"ans_{r['id']}", height=120)
            if st.button("📧 Отправить на email", key=f"send_{r['id']}"):
                ok = _send(r["email"],
                           f"MyContractAnalyzer: ответ по обращению «{r['topic']}»",
                           f"Здравствуйте!\n\n{answer}\n\nС уважением,\nподдержка MyContractAnalyzer.")
                if ok:
                    conn = get_connection()
                    conn.execute("UPDATE support_messages SET replied=1 WHERE id=?", (r["id"],))
                    conn.commit()
                    conn.close()
                    st.success("Отправлено!")
                    st.rerun()
                else:
                    st.error("Не удалось отправить (проверь GMAIL-секреты на сервере)")