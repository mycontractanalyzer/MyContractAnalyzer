THEME_CSS = """
<style>
/* ============ MCA THEME FIX 3.0 ============ */

/* ---- читаемый текст на золотых кнопках ---- */
div.stButton>button, div.stDownloadButton>button,
div.stButton>button p, div.stButton>button span,
div.stDownloadButton>button p, div.stDownloadButton>button span{
color:#241503 !important;text-shadow:none !important;font-weight:800 !important;letter-spacing:.2px;}

/* ---- карточки подписок: контур жирнее и белее ---- */
div[data-testid="stVerticalBlockBorderWrapper"]{
border:1.5px solid rgba(255,255,255,.30) !important;}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{
border-color:rgba(255,255,255,.55) !important;box-shadow:0 18px 60px rgba(255,255,255,.06) !important;}

/* ---- орбы тише и медленнее (чтобы не «светилось в углу») ---- */
.mca-bg::before{background:radial-gradient(circle,rgba(240,180,41,.10),transparent 60%) !important;filter:blur(140px) !important;animation-duration:26s !important;}
.mca-bg::after{background:radial-gradient(circle,rgba(93,120,255,.08),transparent 60%) !important;filter:blur(140px) !important;animation-duration:30s !important;}

/* ---- меню ☰ — фиксированно в правом верхнем углу, как шапка сайта ---- */
div[data-testid="stPopover"]{position:fixed !important;top:14px;right:18px;z-index:999999;}

/* ---- золотая линия сверху (фирменный штрих) ---- */
body::after{content:"";position:fixed;top:0;left:0;right:0;height:3px;
background:linear-gradient(90deg,transparent,#f0b429 30%,#ffd97a 50%,#f0b429 70%,transparent);
z-index:1000000;opacity:.85;pointer-events:none;}

/* ---- вопросы FAQ и абзацы-заголовки — золотом ---- */
section.main p:has(> strong:first-child){color:#ffd166 !important;font-size:17px;margin-bottom:2px;}
</style>
"""