import streamlit as st

from core.i18n import t
from core.ui import render_header

render_header()

st.title(t("settings_title"))

lang = st.selectbox(
    t("language"),
    ["ru", "en"],
    index=0 if st.session_state.get("lang", "ru") == "ru" else 1,
    format_func=lambda x: "Русский" if x == "ru" else "English",
)
if lang != st.session_state.get("lang", "ru"):
    st.session_state["lang"] = lang
    st.rerun()

st.selectbox(
    t("theme"),
    ["dark"],
    format_func=lambda x: "🌙 Тёмная",
    disabled=True,
    help="Личный переключатель темы появится в обновлении. Сейчас тема общая — в .streamlit/config.toml",
)

st.divider()
st.subheader("📄 Документы")
st.toggle(t("pdf_logo"), value=True, disabled=True, help="Заработает вместе с PDF-экспортом")

st.subheader("✉️ Уведомления")
st.toggle(t("email_notif"), value=True, disabled=True, help="Напоминания о продлении подписки — скоро")

st.divider()
st.subheader("Скоро в настройках")
st.write("• 🔐 Смена пароля")
st.write("• 🗑️ Удаление аккаунта и данных")
st.write("• 🔗 Привязка Google-аккаунта")
st.write("• 👥 Командный доступ (для Business)")