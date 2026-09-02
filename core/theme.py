THEME_CSS = """
<style>
/* ================= MCA THEME 2.0 ================= */

/* ---- фон: убираем старые «звёзды», включаем два живых орба ---- */
.mca-bg{background:none !important;animation:none !important;opacity:1 !important;}
.mca-bg::before,.mca-bg::after{content:"";position:fixed;border-radius:50%;filter:blur(120px);z-index:-1;pointer-events:none;}
.mca-bg::before{width:60vw;height:60vw;left:-18vw;top:-22vw;background:radial-gradient(circle,rgba(240,180,41,.17),transparent 62%);animation:mcaOrb1 18s ease-in-out infinite alternate;}
.mca-bg::after{width:52vw;height:52vw;right:-16vw;bottom:-18vw;background:radial-gradient(circle,rgba(93,120,255,.13),transparent 60%);animation:mcaOrb2 22s ease-in-out infinite alternate-reverse;}
@keyframes mcaOrb1{from{transform:translate3d(0,0,0) scale(1);}to{transform:translate3d(5vw,4vw,0) scale(1.15);}}
@keyframes mcaOrb2{from{transform:translate3d(0,0,0) scale(1.1);}to{transform:translate3d(-4vw,-3vw,0) scale(1);}}

html,body,#root,.stApp,.stAppViewContainer,section.main,
div[data-testid="stAppView"],div[data-testid="stMainBlockContainer"]{background:#05060a !important;}
::selection{background:rgba(240,180,41,.35);color:#fff;}

body,p,li{color:#c9ced9;}
a{color:#ffd166 !important;}
h1,h2,h3,h4{color:#f4f6fa !important;}
h2::after{content:"";display:block;width:56px;height:3px;border-radius:99px;margin-top:8px;background:linear-gradient(90deg,#f0b429,transparent);}

@keyframes mcaFadeUp{from{opacity:0;transform:translateY(24px);}to{opacity:1;transform:none;}}
@keyframes mcaShine{to{background-position:200% center;}}
@keyframes mcaGlow{0%,100%{box-shadow:0 0 45px rgba(240,180,41,.22);}50%{box-shadow:0 0 90px rgba(240,180,41,.5);}}

/* лесенка появления блоков */
section.main .stVerticalBlock > *{animation:mcaFadeUp .6s cubic-bezier(.22,1,.36,1) both;}
section.main .stVerticalBlock > *:nth-child(2){animation-delay:.07s;}
section.main .stVerticalBlock > *:nth-child(3){animation-delay:.14s;}
section.main .stVerticalBlock > *:nth-child(4){animation-delay:.21s;}
section.main .stVerticalBlock > *:nth-child(5){animation-delay:.28s;}
section.main .stVerticalBlock > *:nth-child(6){animation-delay:.35s;}
section.main .stVerticalBlock > *:nth-child(7){animation-delay:.42s;}
section.main .stVerticalBlock > *:nth-child(8){animation-delay:.49s;}

/* ---- герой ---- */
.mca-hero-wrap{gap:46px !important;margin:20px auto 42px !important;animation:mcaFadeUp .9s cubic-bezier(.22,1,.36,1) both !important;}
.mca-logo{width:200px !important;height:200px !important;border-radius:50%;animation:mcaGlow 4.5s ease-in-out infinite !important;}
.mca-hero-fallback{font-size:100px;}
.mca-hero-box{border:1.5px solid transparent !important;border-radius:28px !important;padding:28px 52px !important;
background:linear-gradient(#0a0c12,#0a0c12) padding-box,
linear-gradient(115deg,rgba(240,180,41,.9),rgba(255,255,255,.15) 45%,rgba(240,180,41,.5)) border-box !important;
box-shadow:0 24px 80px rgba(0,0,0,.5) !important;backdrop-filter:blur(8px);}
.mca-hero-box h1{font-size:42px !important;background:linear-gradient(90deg,#ffffff,#ffd97a 45%,#ffffff 90%);background-size:200%;
-webkit-background-clip:text;background-clip:text;color:transparent !important;animation:mcaShine 7s linear infinite !important;}
.mca-slogan{letter-spacing:6px !important;color:#f5c044 !important;font-weight:800 !important;}

/* ---- карточки ---- */
div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:22px !important;border:1px solid rgba(255,255,255,.09) !important;
background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.015)) !important;
box-shadow:0 12px 44px rgba(0,0,0,.35) !important;transition:transform .3s ease,border-color .3s ease,box-shadow .3s ease !important;}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-4px);border-color:rgba(240,180,41,.5) !important;box-shadow:0 18px 60px rgba(240,180,41,.12) !important;}

/* ---- кнопки ---- */
div.stButton>button,div.stDownloadButton>button{border-radius:14px !important;border:none !important;
background:linear-gradient(135deg,#ffd166,#f0a71b 55%,#dd8f12) !important;color:#181004 !important;font-weight:800 !important;
box-shadow:0 6px 22px rgba(240,167,27,.22) !important;transition:transform .22s ease,box-shadow .22s ease,filter .22s ease !important;}
div.stButton>button:hover,div.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 34px rgba(240,167,27,.45) !important;filter:brightness(1.06);}
div.stButton>button:active{transform:translateY(0) scale(.99);}

/* ---- поля ввода ---- */
div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div,div[data-testid="stNumberInput"] input{
background:rgba(255,255,255,.05) !important;border:1px solid rgba(255,255,255,.12) !important;border-radius:12px !important;
color:#eef1f6 !important;transition:border-color .2s ease,box-shadow .2s ease,background .2s ease !important;}
div[data-testid="stTextInput"] input:focus,div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stSelectbox"] > div:focus-within,div[data-testid="stNumberInput"] input:focus{
border-color:rgba(240,180,41,.75) !important;box-shadow:0 0 0 4px rgba(240,180,41,.14) !important;background:rgba(255,255,255,.07) !important;}
input[type="radio"],input[type="checkbox"]{accent-color:#f0b429;}

/* ---- экспандеры / вкладки / метрики ---- */
div[data-testid="stExpander"]{border:1px solid rgba(255,255,255,.09) !important;border-radius:16px !important;background:rgba(255,255,255,.025) !important;transition:border-color .25s ease !important;}
div[data-testid="stExpander"]:hover{border-color:rgba(240,180,41,.4) !important;}
div[data-testid="stExpander"] summary{font-weight:700;color:#e8ebf2;}
div[data-testid="stTabs"] button{color:#98a0ae;font-weight:700;border-radius:10px;transition:color .2s ease,background .2s ease;}
div[data-testid="stTabs"] button:hover{color:#ffd166;background:rgba(240,180,41,.07);}
div[data-testid="stTabs"] button[aria-selected="true"]{color:#ffd166 !important;background:rgba(240,180,41,.10) !important;}
div[data-testid="stMetric"]{background:linear-gradient(180deg,rgba(240,180,41,.10),rgba(240,180,41,.02)) !important;border:1px solid rgba(240,180,41,.3) !important;border-radius:18px !important;padding:14px 20px !important;box-shadow:0 8px 30px rgba(0,0,0,.25) !important;}
div[data-testid="stMetric"] label{color:#ffd166 !important;}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#fff !important;}

/* ---- алерты / цитаты / код / прогресс / меню ---- */
div[data-testid="stError"],div[data-testid="stWarning"],div[data-testid="stSuccess"],div[data-testid="stInfo"]{border-radius:14px !important;}
blockquote{border-left:3px solid #f0b429 !important;background:rgba(240,180,41,.07) !important;border-radius:0 12px 12px 0 !important;padding:10px 18px !important;color:#d9dde6 !important;}
pre{border-radius:14px !important;border:1px solid rgba(255,255,255,.08) !important;}
div[data-testid="stProgress"] > div{background:rgba(255,255,255,.08) !important;border-radius:99px !important;}
div[data-testid="stProgress"] > div > div{background:linear-gradient(90deg,#ffd166,#f0a71b) !important;border-radius:99px !important;transition:width .6s ease !important;}
div[data-testid="stPopover"] button{border-radius:12px !important;border:1px solid rgba(240,180,41,.4) !important;background:rgba(240,180,41,.08) !important;transition:all .25s ease !important;}
div[data-testid="stPopover"] button:hover{background:rgba(240,180,41,.16) !important;box-shadow:0 0 20px rgba(240,180,41,.25) !important;}

/* ---- скроллбар ---- */
::-webkit-scrollbar{width:10px;height:10px;}
::-webkit-scrollbar-thumb{background:rgba(240,180,41,.35);border-radius:99px;}
::-webkit-scrollbar-thumb:hover{background:rgba(240,180,41,.55);}
::-webkit-scrollbar-track{background:transparent;}

@media (prefers-reduced-motion: reduce){*{animation:none !important;transition:none !important;}}

/* ---- мобильная версия ---- */
@media (max-width:720px){
  .mca-hero-wrap{flex-direction:column !important;gap:16px !important;margin:8px 8px 24px !important;}
  .mca-logo{width:112px !important;height:112px !important;}
  .mca-hero-box{padding:18px 20px !important;border-radius:20px !important;width:100%;box-sizing:border-box;text-align:center;}
  .mca-hero-box h1{font-size:22px !important;}
  .mca-slogan{font-size:9px !important;letter-spacing:3px !important;}
  div[data-testid="stHorizontalBlock"]{flex-direction:column !important;gap:12px !important;}
  div[data-testid="stHorizontalBlock"] > div{width:100% !important;}
  h1{font-size:24px !important;} h2{font-size:20px !important;} h3{font-size:17px !important;}
}
</style>
"""