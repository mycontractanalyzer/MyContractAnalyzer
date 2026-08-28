import streamlit as st

STRINGS = {
    "ru": {
        "menu_home": "🏠 Главная страница",
        "menu_auth": "🔐 Авторизация",
        "menu_upload": "📄 Загрузка договора",
        "menu_chat": "💬 Анализ и чат",
        "menu_profile": "👤 Личный кабинет",
        "menu_settings": "⚙️ Настройки",
        "menu_admin": "🛠️ Админка",
        "hero_title": "Посмотрите, что вы подписываете",
        "hero_sub": "AI-анализ договоров простым языком",
        "settings_title": "⚙️ Настройки",
        "language": "Язык / Language",
        "theme": "Тема оформления",
        "pdf_logo": "Логотип на PDF-отчётах",
        "email_notif": "Email-уведомления",
        "pricing": "💳 Тарифы",
    },
    "en": {
        "menu_home": "🏠 Home",
        "menu_auth": "🔐 Sign in",
        "menu_upload": "📄 Upload contract",
        "menu_chat": "💬 Analysis & chat",
        "menu_profile": "👤 Account",
        "menu_settings": "⚙️ Settings",
        "menu_admin": "🛠️ Admin",
        "hero_title": "See what you're signing",
        "hero_sub": "Plain-language AI contract analysis",
        "settings_title": "⚙️ Settings",
        "language": "Language / Язык",
        "theme": "Theme",
        "pdf_logo": "Logo on PDF reports",
        "email_notif": "Email notifications",
        "pricing": "💳 Pricing",
    },
}


def t(key: str) -> str:
    lang = st.session_state.get("lang", "ru")
    return STRINGS.get(lang, STRINGS["ru"]).get(key, STRINGS["ru"].get(key, key))