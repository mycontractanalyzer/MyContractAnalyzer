THEME_CSS = """
<style>
/* ================= MCA DESIGN v4 + HOMEPAGE ================= */
section.main .stVerticalBlock{gap:1.3rem;}
.block-container{max-width:1400px !important;width:100% !important;padding-left:2.4rem !important;padding-right:2.4rem !important;}
@media (max-width:720px){.block-container{padding-left:1rem !important;padding-right:1rem !important;}}

div[data-testid="stVerticalBlockBorderWrapper"]{
backdrop-filter:blur(12px);
border:1px solid rgba(255,255,255,.10) !important;
background:linear-gradient(160deg,rgba(255,255,255,.07),rgba(255,255,255,.02) 60%) !important;
box-shadow:0 18px 60px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.08) !important;
transition:transform .35s cubic-bezier(.22,1,.36,1), box-shadow .35s, border-color .35s !important;}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-5px);border-color:rgba(240,180,41,.55) !important;
box-shadow:0 26px 80px rgba(240,167,27,.16), inset 0 1px 0 rgba(255,255,255,.12) !important;}

div.stButton>button,div.stDownloadButton>button{padding:14px 26px !important;font-size:15px !important;
box-shadow:0 8px 26px rgba(240,167,27,.28), inset 0 1px 0 rgba(255,255,255,.5) !important;}
div.stButton>button:hover{box-shadow:0 14px 40px rgba(240,167,27,.5), inset 0 1px 0 rgba(255,255,255,.6) !important;}

h1{background:linear-gradient(92deg,#ffffff,#ffd97a 45%,#ffffff 80%);background-size:220%;
-webkit-background-clip:text;background-clip:text;color:transparent !important;animation:mcaShine 8s linear infinite;
text-shadow:0 0 60px rgba(240,180,41,.25);}
h2{letter-spacing:.3px;}

div[data-testid="stPopover"] > div{border-radius:20px !important;overflow:hidden;background:rgba(11,14,20,.92) !important;
backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.12) !important;box-shadow:0 30px 90px rgba(0,0,0,.65) !important;}
div[data-testid="stPopover"] button{border-radius:0 !important;border:none !important;border-bottom:1px solid rgba(255,255,255,.05) !important;
background:transparent !important;color:#e8ebf2 !important;justify-content:flex-start !important;padding:13px 20px !important;font-weight:600 !important;}
div[data-testid="stPopover"] button:hover{background:rgba(240,180,41,.12) !important;color:#ffd166 !important;}

div[data-testid="stTabs"] > div{border-bottom:1px solid rgba(255,255,255,.08);}
div[data-testid="stMetric"]{backdrop-filter:blur(8px);}

/* ===== SUPPORT BUBBLE ===== */
.mca-support-bubble{position:fixed;bottom:24px;right:24px;z-index:99999;display:flex;align-items:center;gap:10px;
background:linear-gradient(135deg,#ffd166,#f0a71b);color:#181004 !important;text-decoration:none !important;
font-weight:800;padding:14px 22px;border-radius:999px;font-size:15px;cursor:pointer;
box-shadow:0 12px 34px rgba(240,167,27,.5), inset 0 1px 0 rgba(255,255,255,.5);
transition:transform .22s ease, box-shadow .22s ease;animation:mcaFadeUp .8s .4s cubic-bezier(.22,1,.36,1) both;}
.mca-support-bubble:hover{transform:translateY(-4px) scale(1.04);box-shadow:0 18px 48px rgba(240,167,27,.65);color:#181004 !important;}
.mca-support-bubble:active{transform:scale(.98);}
@media (max-width:720px){.mca-support-bubble{bottom:14px;right:14px;padding:12px 18px;font-size:14px;}}

/* ===== HERO SUBTITLE ===== */
.mca-hero-sub{margin-top:14px;font-size:18px;color:#c9ced9;font-weight:500;letter-spacing:.3px;max-width:640px;}
.mca-hero-cta{margin-top:28px;display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}

/* ===== STATISTICS STRIP ===== */
.mca-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:40px 0;}
.mca-stat{padding:22px 18px;text-align:center;border-radius:18px;
background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.015));
border:1px solid rgba(255,255,255,.09);backdrop-filter:blur(8px);
transition:all .3s ease;}
.mca-stat:hover{transform:translateY(-3px);border-color:rgba(240,180,41,.5);
box-shadow:0 14px 40px rgba(240,167,27,.18);}
.mca-stat-value{font-family:'Unbounded',sans-serif;font-size:32px;font-weight:800;
background:linear-gradient(92deg,#ffd166,#fff);-webkit-background-clip:text;background-clip:text;color:transparent;
line-height:1;}
.mca-stat-label{margin-top:6px;font-size:13px;color:#98a0ae;letter-spacing:.4px;text-transform:uppercase;}
@media (max-width:720px){.mca-stats{grid-template-columns:repeat(2,1fr);}.mca-stat-value{font-size:24px;}}

/* ===== STEP CARDS ===== */
.mca-step{position:relative;padding:28px 24px 24px;border-radius:22px;
background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.01));
border:1px solid rgba(255,255,255,.10);backdrop-filter:blur(10px);
transition:all .35s cubic-bezier(.22,1,.36,1);overflow:hidden;min-height:180px;}
.mca-step::before{content:"";position:absolute;top:-60px;right:-60px;width:140px;height:140px;border-radius:50%;
background:radial-gradient(circle,rgba(240,180,41,.18),transparent 60%);filter:blur(20px);pointer-events:none;}
.mca-step:hover{transform:translateY(-6px);border-color:rgba(240,180,41,.55);
box-shadow:0 24px 70px rgba(240,167,27,.2);}
.mca-step-num{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;
background:linear-gradient(135deg,#ffd166,#f0a71b);color:#181004;font-weight:800;font-size:18px;
box-shadow:0 6px 20px rgba(240,167,27,.4);margin-bottom:14px;}
.mca-step h3{font-size:18px !important;color:#fff !important;margin:0 0 10px 0 !important;font-family:'Unbounded',sans-serif;}
.mca-step p{margin:0;color:#c9ced9;font-size:14.5px;line-height:1.55;}

/* ===== DOCTYPE CARDS ===== */
.mca-doctype{padding:22px;border-radius:18px;min-height:130px;
background:linear-gradient(160deg,rgba(255,255,255,.05),rgba(255,255,255,.01));
border:1px solid rgba(255,255,255,.09);backdrop-filter:blur(8px);
transition:all .3s ease;position:relative;}
.mca-doctype:hover{transform:translateY(-4px);border-color:rgba(240,180,41,.5);
box-shadow:0 16px 50px rgba(240,167,27,.15);}
.mca-doctype-icon{font-size:28px;margin-bottom:8px;}
.mca-doctype h4{font-size:15px !important;color:#ffd166 !important;margin:0 0 6px 0 !important;font-family:'Unbounded',sans-serif;font-weight:700;}
.mca-doctype p{margin:0;color:#b8bfcc;font-size:13.5px;line-height:1.5;}

/* ===== BENEFIT CARDS ===== */
.mca-benefit{padding:26px 22px;border-radius:20px;min-height:160px;
background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.01));
border:1px solid rgba(255,255,255,.10);backdrop-filter:blur(10px);transition:all .35s ease;}
.mca-benefit:hover{transform:translateY(-5px);border-color:rgba(240,180,41,.55);
box-shadow:0 20px 60px rgba(240,167,27,.18);}
.mca-benefit-icon{font-size:32px;margin-bottom:12px;display:inline-block;}
.mca-benefit h4{font-size:17px !important;color:#fff !important;margin:0 0 10px 0 !important;font-family:'Unbounded',sans-serif;}
.mca-benefit p{margin:0;color:#c9ced9;font-size:14.5px;line-height:1.55;}

/* ===== REVIEWS ===== */
.mca-review{padding:22px;border-radius:18px;
background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.015));
border:1px solid rgba(255,255,255,.10);backdrop-filter:blur(8px);min-height:140px;transition:all .3s ease;}
.mca-review:hover{border-color:rgba(240,180,41,.4);}
.mca-review-author{font-size:13px;color:#ffd166;font-weight:700;margin-bottom:8px;letter-spacing:.3px;}
.mca-review > div:last-child{color:#c9ced9;font-size:14.5px;line-height:1.6;font-style:italic;}

/* ===== FAQ ===== */
.mca-faq{padding:18px 22px;margin-bottom:10px;border-radius:14px;
background:linear-gradient(160deg,rgba(255,255,255,.04),rgba(255,255,255,.01));
border:1px solid rgba(255,255,255,.08);backdrop-filter:blur(6px);transition:all .25s ease;}
.mca-faq:hover{border-color:rgba(240,180,41,.35);transform:translateX(2px);}
.mca-faq-q{font-weight:700;color:#ffd166;font-size:15.5px;margin-bottom:8px;font-family:'Unbounded',sans-serif;}
.mca-faq > div:last-child{color:#c9ced9;font-size:14.5px;line-height:1.6;}

/* ===== SECTION HEADER ===== */
.mca-section-head{text-align:center;margin:24px 0 8px;}
.mca-section-head h2{font-size:32px !important;font-family:'Unbounded',sans-serif;margin:0 !important;
background:linear-gradient(92deg,#fff,#ffd97a 50%,#fff);background-size:200%;
-webkit-background-clip:text;background-clip:text;color:transparent;animation:mcaShine 9s linear infinite;}
.mca-section-head p{color:#98a0ae;font-size:15px;margin-top:10px;}
@media (max-width:720px){.mca-section-head h2{font-size:24px !important;}}

/* ===== DIVIDER ===== */
hr{border:none !important;height:1px !important;margin:40px 0 !important;
background:linear-gradient(90deg,transparent,rgba(240,180,41,.35),transparent) !important;}

@media (max-width:720px){
  .mca-hero-sub{font-size:15px;}
  div[data-testid="stHorizontalBlock"]{flex-direction:column !important;gap:12px !important;}
  div[data-testid="stHorizontalBlock"] > div{width:100% !important;}
}
</style>
"""