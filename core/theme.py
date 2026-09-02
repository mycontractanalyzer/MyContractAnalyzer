THEME_CSS = """
<style>
/* ============ MCA THEME FIX 3.1 ============ */

/* читаемый текст на золотых кнопках */
div.stButton>button, div.stDownloadButton>button,
div.stButton>button p, div.stButton>button span,
div.stDownloadButton>button p, div.stDownloadButton>button span{
color:#241503 !important;text-shadow:none !important;font-weight:800 !important;letter-spacing:.2px;}

/* карточки подписок: контур жирнее и белее */
div[data-testid="stVerticalBlockBorderWrapper"]{
border:1.5px solid rgba(255,255,255,.30) !important;}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{
border-color:rgba(255,255,255,.55) !important;box-shadow:0 18px 60px rgba(255,255,255,.06) !important;}

/* орбы тише и медленнее */
.mca-bg::before{background:radial-gradient(circle,rgba(240,180,41,.10),transparent 60%) !important;filter:blur(140px) !important;animation-duration:26s !important;}
.mca-bg::after{background:radial-gradient(circle,rgba(93,120,255,.08),transparent 60%) !important;filter:blur(140px) !important;animation-duration:30s !important;}

/* золотая линия сверху */
body::after{content:"";position:fixed;top:0;left:0;right:0;height:3px;
background:linear-gradient(90deg,transparent,#f0b429 30%,#ffd97a 50%,#f0b429 70%,transparent);
z-index:1000000;opacity:.85;pointer-events:none;}

/* вопросы FAQ золотом */
section.main p:has(> strong:first-child){color:#ffd166 !important;font-size:17px;margin-bottom:2px;}

/* тосты/уведомления — всегда поверх и всегда видимы */
div[data-testid="stToastContainer"]{z-index:999999 !important;}
div[data-testid="stToast"]{opacity:1 !important;visibility:visible !important;}
</style>
"""