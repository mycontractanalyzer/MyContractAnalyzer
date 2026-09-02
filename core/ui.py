import base64
import os

import streamlit as st

import config
from core.i18n import t
from utils.auth import get_session_user


@st.cache_resource
def _logo_base64():
    p = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


PREMIUM_CSS = """
<style>
#MainMenu, footer, header {display:none !important;}
section[data-testid="stSidebar"] {display:none;}

/* ==== ФОН: глубина + два «дышащих» орба ==== */
html, body, #root, .stApp, .stAppViewContainer, section.main,
div[data-testid="stAppView"], div[data-testid="stMainBlockContainer"] {background:#07080c !important;}
.mca-bg{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none;}
.mca-bg .orb{position:absolute;border-radius:50%;filter:blur(110px);opacity:.55;}
.mca-bg .o1{width:55vw;height:55vw;left:-15vw;top:-20vw;background:radial-gradient(circle, rgba(240,180,41,.20), transparent 62%);animation:orbFloat 16s ease-in-out infinite alternate;}
.mca-bg .o2{width:48vw;height:48vw;right:-14vw;bottom:-16vw;background:radial-gradient(circle, rgba(88,120,255,.14), transparent 60%);animation:orbFloat 20s ease-in-out infinite alternate-reverse;}
@keyframes orbFloat{from{transform:translate3d(0,0,0) scale(1);}to{transform:translate3d(6vw,4vw,0) scale(1.12);}}

/* ==== ТИПОГРАФИКА ==== */
body,p,li,span,div{font-family:'Manrope',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;}
h1,h2,h3,h4{font-family:'Unbounded',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#f4f6fa !important;letter-spacing:.2px;}
p,li{color:#c9ced9;}
a{color:#ffd166 !important;}

@keyframes fadeUp{from{opacity:0;transform:translateY(22px);}to{opacity:1;transform:none;}}
@keyframes shine{to{background-position:200% center;}}
@keyframes ringspin{to{transform:rotate(360deg);}}

/* лесенка появления блоков */
section.main .stVerticalBlock > *{animation:fadeUp .55s cubic-bezier(.22,1,.36,1) both;}
section.main .stVerticalBlock > *:nth-child(2){animation-delay:.06s;}
section.main .stVerticalBlock > *:nth-child(3){animation-delay:.12s;}
section.main .stVerticalBlock > *:nth-child(4){animation-delay:.18s;}
section.main .stVerticalBlock > *:nth-child(5){animation-delay:.24s;}
section.main .stVerticalBlock > *:nth-child(6){animation-delay:.30s;}
section.main .stVerticalBlock > *:nth-child(7){animation-delay:.36s;}
section.main .stVerticalBlock > *:nth-child(8){animation-delay:.42s;}

/* ==== ГЕРОЙ ==== */
.mca-hero-wrap{display:flex;align-items:center;justify-content:center;gap:46px;margin:14px auto 34px;animation:fadeUp .8s cubic-bezier(.22,1,.36,1) both;}
.mca-logo-wrap{position:relative;border-radius:50%;flex-shrink:0;}
.mca-logo-wrap::before{content:"";position:absolute;inset:-6px;border-radius:50%;background:conic-gradient(rgba(240,180,41,.9) 0 12%, transparent 18% 46%, rgba(240,180,41,.7) 52% 68%, transparent 74% 100%);filter:blur(7px);animation:ringspin 7s linear infinite;}
.mca-logo{position:relative;width:205px;height:205px;border-radius:50%;object-fit:cover;box-shadow:0 0 70px rgba(240,180,41,.28);}
.mca-hero-fallback{font-size:96px;position:relative;}
.mca-hero-box{border-radius:26px;padding:26px 50px;border:1.5px solid transparent;background:linear-gradient(#0b0d13,#0b0d13) padding-box,linear-gradient(115deg,rgba(240,180,41,.85),rgba(255,255,255,.18) 45%,rgba(240,180,41,.55)) border-box;box-shadow:0 18px 60px rgba(0,0,0,.45);}
.mca-hero-box h1{font-size:40px;margin:0;background:linear-gradient(90deg,#ffffff,#ffd97a 45%,#ffffff 90%);background-size:200%;-webkit-background-clip:text;background-clip:text;color:transparent !important;animation:shine 7s linear infinite;}
.mca-slogan{margin-top:12px;color:#f0b429;font-size:13px;letter-spacing:5px;text-transform:uppercase;font-weight:800;}

/* ==== КАРТОЧКИ ==== */
div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:22px;border:1px solid rgba(255,255,255,.09);background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.015));box-shadow:0 12px 44px rgba(0,0,0,.35);transition:transform .3s ease,border-color .3s ease,box-shadow .3s ease;}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-4px);border-color:rgba(240,180,41,.45);box-shadow:0 18px 60px rgba(240,180,41,.10);}

/* ==== КНОПКИ ==== */
div.stButton>button,div.stDownloadButton>button{border-radius:14px;border:none;background:linear-gradient(135deg,#ffd166,#f0a71b 55%,#dd8f12);color:#181004;font-weight:800;letter-spacing:.2px;box-shadow:0 6px 22px rgba(240,167,27,.22);transition:transform .22s ease,box-shadow .22s ease,filter .22s ease;}
div.stButton>button:hover,div.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 34px rgba(240,167,27,.4);filter:brightness(1.06);}
div.stButton>button:active{transform:translateY(0) scale(.99);}

/* ==== ПОЛЯ ВВОДА ==== */
div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div,div[data-testid="stNumberInput"] input{
background:rgba(255,255,255,.05)!important;border:1px solid rgba(255,255,255,.12)!important;border-radius:12px;color:#eef1f6 !important;transition:border-color .2s ease,box-shadow .2s ease,background .2s ease;}
div[data-testid="stTextInput"] input:focus,div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stSelectbox"] > div:focus-within,div[data-testid="stNumberInput"] input:focus{
border-color:rgba(240,180,41,.75)!important;box-shadow:0 0 0 4px rgba(240,180,41,.14)!important;background:rgba(255,255,255,.07)!important;}

/* ==== ЭКСПАНДЕРЫ / ВКЛАДКИ / МЕТРИКИ ==== */
div[data-testid="stExpander"]{border:1px solid rgba(255,255,255,.09);border-radius:16px;background:rgba(255,255,255,.025);transition:border-color .25s ease;}
div[data-testid="stExpander"]:hover{border-color:rgba(240,180,41,.4);}
div[data-testid="stExpander"] summary{font-weight:700;color:#e8ebf2;}
div[data-testid="stTabs"] button{color:#98a0ae;font-weight:700;transition:color .2s ease,background .2s ease;border-radius:10px;}
div[data-testid="stTabs"] button:hover{color:#ffd166;background:rgba(240,180,41,.07);}
div[data-testid="stTabs"] button[aria-selected="true"]{color:#ffd166;background:rgba(240,180,41,.10);}
div[data-testid="stMetric"]{background:linear-gradient(180deg,rgba(240,180,41,.10),rgba(240,180,41,.02));border:1px solid rgba(240,180,41,.3);border-radius:18px;padding:14px 20px;box-shadow:0 8px 30px rgba(0,0,0,.25);}
div[data-testid="stMetric"] label{color:#ffd166 !important;}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#fff !important;}

/* ==== АЛЕРТЫ / ЦИТАТЫ / КОД / ПРОГРЕСС ==== */
div[data-testid="stError"],div[data-testid="stWarning"],div[data-testid="stSuccess"],div[data-testid="stInfo"]{border-radius:14px;}
blockquote{border-left:3px solid #f0b429;background:rgba(240,180,41,.07);border-radius:0 12px 12px 0;padding:10px 18px;color:#d9dde6;}
pre{border-radius:14px !important;border:1px solid rgba(255,255,255,.08)!important;}
div[data-testid="stProgress"] > div{background:rgba(255,255,255,.08);border-radius:99px;}
div[data-testid="stProgress"] > div > div{background:linear-gradient(90deg,#ffd166,#f0a71b)!important;border-radius:99px;transition:width .6s ease;}

/* ==== СКРОЛЛБАР ==== */
::-webkit-scrollbar{width:10px;height:10px;}
::-webkit-scrollbar-thumb{background:rgba(240,180,41,.35);border-radius:99px;}
::-webkit-scrollbar-track{background:transparent;}

@media (prefers-reduced-motion: reduce){*{animation:none !important;transition:none !important;}}

/* ==== МОБИЛЬНАЯ ВЕРСИЯ ==== */
@media (max-width:720px){
  .mca-hero-wrap{flex-direction:column;gap:16px;margin:8px 8px 22px;}
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
        PREMIUM_CSS + '<div class="mca-bg"><i class="orb o1"></i><i class="orb o2"></i></div>',
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
  <span class="mca-logo-wrap">{logo_html}</span>
  <div class="mca-hero-box">
    <h1>MyContractAnalyzer</h1>
    <div class="mca-slogan">See what you're signing</div>
  </div>
</div>
""", unsafe_allow_html=True)