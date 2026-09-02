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


PREMIUM_CSS = """
<style>
/* ================= MCA THEME 2.0 ================= */
#MainMenu, footer, header {display:none !important;}
section[data-testid="stSidebar"] {display:none;}

html, body, #root, .stApp, .stAppViewContainer, section.main,
div[data-testid="stAppView"], div[data-testid="stMainBlockContainer"] {background:#05060a !important;}

body, p, li, span, div {font-family:'Manrope',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;}
h1, h2, h3, h4 {font-family:'Unbounded',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#f4f6fa !important;letter-spacing:.2px;}
p, li {color:#c9ced9;}
a {color:#ffd166 !important;}
::selection {background:rgba(240,180,41,.35);color:#fff;}
h2::after {content:"";display:block;width:56px;height:3px;border-radius:99px;margin-top:8px;background:linear-gradient(90deg,#f0b429,transparent);}

.mca-bg{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none;background:none !important;animation:none !important;opacity:1 !important;}
.mca-bg::before,.mca-bg::after{content:"";position:fixed;border-radius:50%;filter:blur(120px);pointer-events:none;}
.mca-bg::before{width:60vw;height:60vw;left:-18vw;top:-22vw;background:radial-gradient(circle,rgba(240,180,41,.17),transparent 62%);animation:mcaOrb1 18s ease-in-out infinite alternate;}
.mca-bg::after{width:52vw;height:52vw;right:-16vw;bottom:-18vw;background:radial-gradient(circle,rgba(93,120,255,.13),transparent 60%);animation:mcaOrb2 22s ease-in-out infinite alternate-reverse;}
@keyframes mcaOrb1{from{transform:translate3d(0,0,0) scale(1);}to{transform:translate3d(5vw,4vw,0) scale(1.15);}}
@keyframes mcaOrb2{from{transform:translate3d(0,0,0) scale(1.1);}to{transform:translate3d(-4vw,-3vw,0) scale(1);}}

@keyframes mcaFadeUp{from{opacity:0;transform:translateY(24px);}to{opacity:1;transform:none;}}
@keyframes mcaShine{to{background-position:200% center;}}
@keyframes mcaGlow{0%,100%{box-shadow:0 0 45px rgba(240,180,41,.22);}50%{box-shadow:0 0 90px rgba(240,180,41,.5);}}

section.main .stVerticalBlock > *{animation:mcaFadeUp .6s cubic-bezier(.22,1,.36,1) both;}
section.main .stVerticalBlock > *:nth-child(2){animation-delay:.07s;}
section.main .stVerticalBlock > *:nth-child(3){animation-delay:.14s;}
section.main .stVerticalBlock > *:nth-child(4){animation-delay:.21s;}
section.main .stVerticalBlock > *:nth-child(5){animation-delay:.28s;}
section.main .stVerticalBlock > *:nth-child(6){animation-delay:.35s;}
section.main .stVerticalBlock > *:nth-child(7){animation-delay:.42s;}
section.main .stVerticalBlock > *:nth-child(8){animation-delay:.49s;}

.mca-hero-wrap{display:flex;align-items:center;justify-content:center;gap:46px;margin:20px auto 42px;animation:mcaFadeUp .9s cubic-bezier(.22,1,.36,1) both;}
.mca-logo{width:200px;height:200px;border-radius:50%;object-fit:cover;animation:mcaGlow 4.5s ease-in-out infinite;}
.mca-hero-fallback{font-size:100px;}
.mca-hero-box{border:1.5px solid transparent;border-radius:28px;padding:28px 52px;
background:linear-gradient(#0a0c12,#0a0c12) padding-box,
linear-gradient(115deg,rgba(240,180,41,.9),rgba(255,255,255,.15) 45%,rgba(240,180,41,.5)) border-box;
box-shadow:0 24px 80px rgba(0,0,0,.5);backdrop-filter:blur(8px);}
.mca-hero-box h1{font-size:42px;margin:0;background:linear-gradient(90deg,#ffffff,#ffd97a 45%,#ffffff 90%);background-size:200%;
-webkit-background-clip:text;background-clip:text;color:transparent !important;animation:mcaShine 7s linear infinite;}
.mca-slogan{margin-top:12px;color:#f5c044;font-size:13px;letter-spacing:6px;text-transform:uppercase;font-weight:800;}

div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:22px !important;border:1px solid rgba(255,255,255,.09) !important;
background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.015)) !important;
box-shadow:0 12px 44px rgba(0,0,0,.35) !important;transition:transform .3s ease,border-color .3s ease,box-shadow .3s ease !important;}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-4px);border-color:rgba(240,180,41,.5) !important;box-shadow:0 18px 60px rgba(240,180,41,.12) !important;}

div.stButton>button,div.stDownloadButton>button{border-radius:14px !important;border:none !important;
background:linear-gradient(135deg,#ffd166,#f0a71b 55%,#dd8f12) !important;color:#181004 !important;font-weight:800 !important;
box-shadow:0 6px 22px rgba(240,167,27,.22) !important;transition:transform .22s ease,box-shadow .22s ease,filter .22s ease !important;}
div.stButton>button:hover,div.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 34px rgba(240,167,27,.45) !important;filter:brightness(1.06);}
div.stButton>button:active{transform:translateY(0) scale(.99);}

div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div,div[data-testid="stNumberInput"] input{
background:rgba(255,255,255,.05) !important;border:1px solid rgba(255,255,255,.12) !important;border-radius:12px !important;
color:#eef1f6 !important;transition:border-color .2s ease,box-shadow .2s ease,background .2s ease !important;}
div[data-testid="stTextInput"] input:focus,div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stSelectbox"] > div:focus-within,div[data-testid="stNumberInput"] input:focus{
border-color:rgba(240,180,41,.75) !important;box-shadow:0 0 0 4px rgba(240,180,41,.14) !important;background:rgba(255,255,255,.07) !important;}
input[type="radio"],input[type="checkbox"]{accent-color:#f0b429;}

div[data-testid="stExpander"]{border:1px solid rgba(255,255,255,.09) !important;border-radius:16px !important;background:rgba(255,255,255,.025) !important;transition:border-color .25s ease !important;}
div[data-testid="stExpander"]:hover{border-color:rgba(240,180,41,.4) !important;}
div[data-testid="stExpander"] summary{font-weight:700;color:#e8ebf2;}
div[data-testid="stTabs"] button{color:#98a0ae;font-weight:700;border-radius:10px;transition:color .2s ease,background .2s ease;}
div[data-testid="stTabs"] button:hover{color:#ffd166;background:rgba(240,180,41,.07);}
div[data-testid="stTabs"] button[aria-selected="true"]{color:#ffd166 !important;background:rgba(240,180,41,.10) !important;}
div[data-testid="stMetric"]{background:linear-gradient(180deg,rgba(240,180,41,.10),rgba(240,180,41,.02)) !important;border:1px solid rgba(240,180,41,.3) !important;border-radius:18px !important;padding:14px 20px !important;box-shadow:0 8px 30px rgba(0,0,0,.25) !important;}
div[data-testid="stMetric"] label{color:#ffd166 !important;}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#fff !important;}

div[data-testid="stError"],div[data-testid="stWarning"],div[data-testid="stSuccess"],div[data-testid="stInfo"]{border-radius:14px !important;}
blockquote{border-left:3px solid #f0b429 !important;background:rgba(240,180,41,.07) !important;border-radius:0 12px 12px 0 !important;padding:10px 18px !important;color:#d9dde6 !important;}
pre{border-radius:14px !important;border:1px solid rgba(255,255,255,.08) !important;}
div[data-testid="stProgress"] > div{background:rgba(255,255,255,.08) !important;border-radius:99px !important;}
div[data-testid="stProgress"] > div > div{background:linear-gradient(90deg,#ffd166,#f0a71b) !important;border-radius:99px !important;transition:width .6s ease !important;}
div[data-testid="stPopover"] button{border-radius:12px !important;border:1px solid rgba(240,180,41,.4) !important;background:rgba(240,180,41,.08) !important;transition:all .25s ease !important;}
div[data-testid="stPopover"] button:hover{background:rgba(240,180,41,.16) !important;box-shadow:0 0 20px rgba(240,180,41,.25) !important;}

::-webkit-scrollbar{width:10px;height:10px;}
::-webkit-scrollbar-thumb{background:rgba(240,180,41,.35);border-radius:99px;}
::-webkit-scrollbar-thumb:hover{background:rgba(240,180,41,.55);}
::-webkit-scrollbar-track{background:transparent;}

@media (prefers-reduced-motion: reduce){*{animation:none !important;transition:none !important;}}

@media (max-width:720px){
  .mca-hero-wrap{flex-direction:column;gap:16px;margin:8px 8px 24px;}
  .mca-logo{width:112px;height:112px;}
  .mca-hero-fallback{font-size:64px;}
  .mca-hero-box{padding:18px 20px;border-radius:20px;width:100%;box-sizing:border-box;text-align:center;}
  .mca-hero-box h1{font-size:22px;}
  .mca-slogan{font-size:9px;letter-spacing:3px;}
  div[data-testid="stHorizontalBlock"]{flex-direction:column !important;gap:12px !important;}
  div[data-testid="stHorizontalBlock"] > div{width:100% !important;}
  .block-container{padding:1rem .9rem !important;}
  h1{font-size:24px !important;} h2{font-size:20px !important;} h3{font-size:17px !important;}
}
@media (min-width:721px) and (max-width:1024px){
  .mca-logo{width:150px;height:150px;}
  .mca-hero-box{padding:20px 28px;}
  .mca-hero-box h1{font-size:27px;}
}
</style>
"""


def inject_style():
    st.markdown(
        PREMIUM_CSS + THEME_CSS + '<div class="mca-bg"></div>',
        unsafe_allow_html=True)


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
        st.page_link("pages/10_lawyers.py", label="🧑‍️ Юристы", use_container_width=True)
        st.page_link("pages/11_library.py", label="🧱 Библиотека пунктов", use_container_width=True)
        st.page_link("pages/12_auto.py", label="🚗 Мир Автовладельца", use_container_width=True)
        st.page_link("pages/13_lawyer247.py", label="🤖 AI-юрист 24/7", use_container_width=True)
        st.page_link("pages/15_podcasts.py", label="🎧 Подкасты", use_container_width=True)
        st.page_link("pages/16_knowledge.py", label="📖 Библиотека знаний", use_container_width=True)
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
        logo_html = (f'<img class="mca-logo" src="data:image/png;base64,{logo}" alt="logo"/>'
                     if logo else '<span class="mca-hero-fallback">⚖️</span>')
    st.markdown(f"""
<div class="mca-hero-wrap">
  {logo_html}
  <div class="mca-hero-box">
    <h1>MyContractAnalyzer</h1>
    <div class="mca-slogan">See what you're signing</div>
  </div>
</div>
""", unsafe_allow_html=True)