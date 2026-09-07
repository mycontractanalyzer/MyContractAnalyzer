import base64
import os

import streamlit as st

import config
from core.i18n import t
from utils.auth import get_session_user

try:
    from core.theme import THEME_CSS
except Exception:
    THEME_CSS = ""


@st.cache_resource
def _logo_base64():
    p = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def inject_style():
    st.markdown(
        THEME_CSS + '<div class="mca-bg"></div><div class="mca-grid"></div>'
        '<a class="mca-support-bubble" href="/14_support">'
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#181004" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
        'Поддержка</a>',
        unsafe_allow_html=True)


def render_menu():
    user = get_session_user()
    with st.popover("☰"):
        st.page_link("app.py", label=t("menu_home"), use_container_width=True)
        if user:
            st.page_link("pages/5_profile.py", label="👤 Личный кабинет", use_container_width=True)
        else:
            st.page_link("pages/1_auth.py", label=t("menu_auth"), use_container_width=True)
        st.page_link("pages/2_dashboard.py", label=t("menu_upload"), use_container_width=True)
        st.page_link("pages/3_result.py", label=t("menu_chat"), use_container_width=True)
        st.page_link("pages/7_settings.py", label="⚙️ Настройки", use_container_width=True)
        st.page_link("pages/7_history.py", label="📚 История", use_container_width=True)
        st.page_link("pages/8_compare.py", label="🆚 Сравнение версий", use_container_width=True)
        st.page_link("pages/10_lawyers.py", label="🧑‍️ Юристы", use_container_width=True)
        st.page_link("pages/12_auto.py", label="🚗 Мир Автовладельца", use_container_width=True)
        st.page_link("pages/13_lawyer247.py", label="🤖 AI-юрист 24/7", use_container_width=True)
        st.page_link("pages/15_podcasts.py", label="🎧 Подкасты", use_container_width=True)
        st.page_link("pages/16_knowledge.py", label="📖 Библиотека знаний", use_container_width=True)
        st.page_link("pages/14_support.py", label="💬 Поддержка", use_container_width=True)
        if user and user["tariff"] in ("Business", "Business Pro"):
            st.page_link("pages/9_company.py", label="🏢 Команда", use_container_width=True)
        if user and user["email"] in config.ADMIN_EMAILS:
            st.page_link("pages/6_admin.py", label=t("menu_admin"), use_container_width=True)
            st.page_link("pages/17_laws.py", label="📚 Загрузчик законов", use_container_width=True)
            st.page_link("pages/18_support_admin.py", label="📨 Поддержка (обращения)", use_container_width=True)
        if user:
            if st.button("🚪 Выйти", key="menu_logout", use_container_width=True):
                from utils.auth import logout_user
                logout_user()
                st.switch_page("app.py")


def render_header():
    inject_style()
    render_menu()


def render_hero():
    static_path = os.path.join(os.path.dirname(__file__), "..", "static", "logo_small.png")
    if os.path.exists(static_path):
        logo_html = '<img class="mca-logo" src="app/static/logo_small.png" alt="logo"/>'
    else:
        logo = _logo_base64()
        logo_html = (f'<img class="mca-logo" src="data:image/png;base64,{logo}" alt="logo"/>'
                     if logo else '<span class="mca-hero-fallback">️</span>')
    st.markdown(f"""
<div class="mca-hero-wrap">
  {logo_html}
  <div class="mca-hero-box">
    <div class="mca-hero-badge">⚖️ AI-юрист для твоих договоров</div>
    <h1>MyContractAnalyzer</h1>
    <div class="mca-slogan">See what you're signing</div>
  </div>
</div>
""", unsafe_allow_html=True)