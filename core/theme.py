THEME_CSS = """
<style>
/* ================= MCA POLISH PACK 3.0 ================= */
section.main .stVerticalBlock{gap:1.15rem;}
.block-container{padding-top:2.2rem;padding-bottom:3.5rem;max-width:1060px;}
div[data-testid="stVerticalBlockBorderWrapper"]{backdrop-filter:blur(10px);transition:all .35s cubic-bezier(.22,1,.36,1);}
div[data-testid="stPopover"] > div{border-radius:18px !important;overflow:hidden;background:#0b0e14 !important;border:1px solid rgba(255,255,255,.10) !important;box-shadow:0 24px 70px rgba(0,0,0,.6) !important;}
div[data-testid="stPopover"] button{border-radius:0 !important;border:none !important;border-bottom:1px solid rgba(255,255,255,.05) !important;background:transparent !important;color:#e8ebf2 !important;justify-content:flex-start !important;padding:12px 18px !important;}
div[data-testid="stPopover"] button:hover{background:rgba(240,180,41,.10) !important;color:#ffd166 !important;}
h1{background:linear-gradient(92deg,#fff,#ffd97a 55%,#fff);background-size:200%;-webkit-background-clip:text;background-clip:text;color:transparent !important;animation:mcaShine 8s linear infinite;}
div[data-testid="stTabs"] > div{border-bottom:1px solid rgba(255,255,255,.08);}
.mca-support-bubble{position:fixed;bottom:22px;right:22px;z-index:9999;display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,#ffd166,#f0a71b);color:#181004;font-weight:800;padding:12px 20px;border-radius:999px;box-shadow:0 10px 30px rgba(240,167,27,.45);text-decoration:none;font-size:15px;transition:transform .2s ease,box-shadow .2s ease;animation:mcaFadeUp .8s .4s cubic-bezier(.22,1,.36,1) both;}
.mca-support-bubble:hover{transform:translateY(-3px) scale(1.03);box-shadow:0 16px 44px rgba(240,167,27,.6);color:#181004;}
@media (max-width:720px){.mca-support-bubble{bottom:14px;right:14px;padding:10px 16px;font-size:14px;}}
</style>
"""