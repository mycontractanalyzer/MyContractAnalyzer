import base64
import os

import streamlit as st

import config
from core.i18n import t
from utils.auth import get_session_user


@st.cache_resource
def _logo_base64():
    base = os.path.join(os.path.dirname(__file__), "..", "assets")
    for name in ("logo.png",):
        p = os.path.join(base, name)
        if os.path.exists(p):
            with open(p, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None


PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&family=Unbounded:wght@400;600&display=swap');

#MainMenu, footer, header {display: none !important;}
section[data-testid="stSidebar"] {display: none;}

html, body, #root, .stApp, .stAppViewContainer, section.main,
div[data-testid="stAppView"], div[data-testid="stMainBlockContainer"],
div[data-testid="stVerticalBlock"] {background-color: #0a0c10 !important;}

body, p, li {font-family: 'Manrope', sans-serif !important;}
h1, h2, h3, h4 {font-family: 'Unbounded', sans-serif !important; color: #fff !important;}
span.material-symbols-rounded {font-family: 'Material Symbols Rounded' !important;}

.mca-bg {position: fixed; inset: 0; z-index: -1; pointer-events: none; opacity: .7;
  background:
    radial-gradient(1.5px 1.5px at 15% 25%, rgba(255,255,255,.5) 50%, transparent 51%),
    radial-gradient(1px 1px at 35% 70%, rgba(255,255,255,.35) 50%, transparent 51%),
    radial-gradient(1.5px 1.5px at 60% 20%, rgba(255,255,255,.4) 50%, transparent 51%),
    radial-gradient(1px 1px at 80% 55%, rgba(255,255,255,.3) 50%, transparent 51%),
    radial-gradient(1px 1px at 45% 45%, rgba(240,180,41,.35) 50%, transparent 51%),
    radial-gradient(1.5px 1.5px at 90% 80%, rgba(255,255,255,.25) 50%, transparent 51%);
  background-size: 900px 700px;
  animation: mcaDrift 90s linear infinite;}
@keyframes mcaDrift {from {background-position: 0 0;} to {background-position: 900px 700px;}}

@keyframes mcaFadeUp {from {opacity: 0; transform: translateY(26px);} to {opacity: 1; transform: none;}}

.mca-hero-wrap {display: flex; align-items: center; justify-content: center; gap: 40px;
  margin: 10px auto 26px; animation: mcaFadeUp .8s ease both;}
.mca-logo {width: 220px; height: 220px; border-radius: 50%; object-fit: cover; flex-shrink: 0;
  margin-left: -50px; box-shadow: 0 0 50px rgba(255,255,255,.18);}
.mca-hero-fallback {font-size: 100px;}
.mca-hero-box {border: 1.5px solid rgba(255,255,255,.85); background: transparent;
  border-radius: 24px; padding: 24px 46px;}
.mca-hero-box h1 {font-size: 38px; margin: 0; color: #fff !important; letter-spacing: .5px;}
.mca-slogan {margin-top: 10px; color: #f0b429; font-size: 14px; letter-spacing: 4px;
  text-transform: uppercase; font-weight: 700;}

[data-testid="stVerticalBlockBorderWrapper"] {
  border: 1px solid rgba(255,255,255,.22) !important;
  border-radius: 20px !important;
  background: rgba(255,255,255,.03) !important;
  transition: all .35s ease !important;}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
  border-color: rgba(240,180,41,.8) !important;
  transform: translateY(-5px);
  box-shadow: 0 14px 44px rgba(240,180,41,.12);}

div.stButton > button {
  background: linear-gradient(135deg, #f0b429, #d19016) !important;
  color: #0a0c10 !important; border: none !important; border-radius: 12px !important;
  font-weight: 700 !important; transition: all .3s ease !important;}
div.stButton > button:hover {box-shadow: 0 0 24px rgba(240,180,41,.45); transform: translateY(-2px);}

.mca-faq {border: 1px solid rgba(255,255,255,.15); border-radius: 14px; padding: 16px 20px; margin-bottom: 10px;
  background: rgba(255,255,255,.02);}
.mca-faq-q {font-weight: 700; color: #f0b429; margin-bottom: 4px;}

.mca-review {border-left: 3px solid #f0b429; padding: 10px 16px; margin: 8px 0;
  background: rgba(240,180,41,.06); border-radius: 0 10px 10px 0;}
.mca-review-author {font-weight: 600;}
</style>
"""

LIGHT_CSS = """
<style>
:root {
  --background-color: #f6f7fb;
  --secondary-background-color: #ffffff;
  --text-color: #171a1f;
  --primary-color: #b07a00;
}
html, body, #root, .stApp, .stAppViewContainer, section.main,
div[data-testid="stAppView"], div[data-testid="stMainBlockContainer"],
div[data-testid="stVerticalBlock"] {background-color: #f6f7fb !important;}
body, p, li, span, label {color: #171a1f !important;}
h1, h2, h3, h4 {color: #111418 !important;}

/* ЧЁРНЫЕ контуры карточек (тарифы, типы договоров) */
[data-testid="stVerticalBlockBorderWrapper"] {
  border: 1.5px solid rgba(0,0,0,.65) !important;
  background: #ffffff !important;}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
  border-color: #b07a00 !important;
  box-shadow: 0 14px 44px rgba(176,122,0,.15);}

.mca-hero-box {border-color: #111418 !important;}
.mca-hero-box h1 {color: #111418 !important;}
.mca-bg {opacity: .12 !important;}

/* FAQ: рамка чёрная, ответы видимые */
.mca-faq {border: 1.5px solid rgba(0,0,0,.55) !important; background: #ffffff !important;}
.mca-faq, .mca-faq div {color: #171a1f !important;}
.mca-faq-q, .mca-faq-q div {color: #b07a00 !important;}

/* Отзывы */
.mca-review {background: rgba(240,180,41,.12) !important; border-left-color: #b07a00 !important;}
.mca-review, .mca-review div {color: #171a1f !important;}
.mca-review-author, .mca-review-author div {color: #111418 !important;}
</style>
"""


def inject_style():
    user = get_session_user()
    theme = (user or {}).get("theme") or "dark"
    css = PREMIUM_CSS + (LIGHT_CSS if theme == "light" else "")
    st.markdown(css + '<div class="mca-bg"></div>', unsafe_allow_html=True)


def render_menu():
    user = get_session_user()
    with st.popover("☰"):
        st.page_link("app.py", label=t("menu_home"), use_container_width=True)
        st.page_link("pages/1_auth.py", label=t("menu_auth"), use_container_width=True)
        st.page_link("pages/2_dashboard.py", label=t("menu_upload"), use_container_width=True)
        st.page_link("pages/3_result.py", label=t("menu_chat"), use_container_width=True)
        st.page_link("pages/5_profile.py", label=t("menu_profile"), use_container_width=True)
        st.page_link("pages/7_settings.py", label="⚙️ Настройки", use_container_width=True)
        st.page_link("pages/7_history.py", label="📚 История", use_container_width=True)
        st.page_link("pages/8_compare.py", label="🆚 Сравнение версий", use_container_width=True)
        if user and user["tariff"] in ("Business", "Business Pro"):
            st.page_link("pages/9_company.py", label="🏢 Команда", use_container_width=True)
        if user and user["email"] in config.ADMIN_EMAILS:
            st.page_link("pages/6_admin.py", label=t("menu_admin"), use_container_width=True)


def render_header():
    inject_style()
    render_menu()


def render_hero():
    static_path = os.path.join(os.path.dirname(__file__), "..", "static", "logo_small.png")
    if os.path.exists(static_path):
        logo_html = '<img class="mca-logo" src="app/static/logo_small.png" alt="logo"/>'
    else:
        logo = _logo_base64()
        if logo:
            logo_html = f'<img class="mca-logo" src="data:image/png;base64,{logo}" alt="logo"/>'
        else:
            logo_html = '<span class="mca-hero-fallback">⚖️</span>'
    st.markdown(f"""
<div class="mca-hero-wrap">
  {logo_html}
  <div class="mca-hero-box">
    <h1>MyContractAnalyzer</h1>
    <div class="mca-slogan">See what you're signing</div>
  </div>
</div>
""", unsafe_allow_html=True)