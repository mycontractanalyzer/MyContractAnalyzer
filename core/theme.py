THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;800&family=Manrope:wght@400;500;700;800&display=swap');

/* ================= MCA BASE ================= */
#MainMenu, footer, header {display:none !important;}
section[data-testid="stSidebar"] {display:none;}

html, body, #root, .stApp, .stAppViewContainer, section.main,
div[data-testid="stAppView"], div[data-testid="stMainBlockContainer"] {background:#05060a !important;}

body, p, li, span, div {font-family:'Manrope',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-weight:500;}
h1, h2, h3, h4 {font-family:'Unbounded',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#f4f6fa !important;letter-spacing:.2px;}
p, li {color:#c9ced9;}
a {color:#ffd166 !important;}
::selection {background:rgba(240,180,41,.35);color:#fff;}
h2::after {content:"";display:block;width:56px;height:3px;border-radius:99px;margin-top:8px;background:linear-gradient(90deg,#f0b429,transparent);}

*:focus{outline:none !important;}

.mca-bg{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none;}
.mca-bg::before,.mca-bg::after{content:"";position:fixed;border-radius:50%;filter:blur(120px);pointer-events:none;}
.mca-bg::before{width:60vw;height:60vw;left:-18vw;top:-22vw;background:radial-gradient(circle,rgba(240,180,41,.17),transparent 62%);animation:mcaOrb1 18s ease-in-out infinite alternate;}
.mca-bg::after{width:52vw;height:52vw;right:-16vw;bottom:-18vw;background:radial-gradient(circle,rgba(93,120,255,.13),transparent 60%);animation:mcaOrb2 22s ease-in-out infinite alternate-reverse;}
.mca-grid{position:fixed;inset:0;z-index:-2;pointer-events:none;
background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);
background-size:64px 64px;mask-image:radial-gradient(ellipse at center,black 25%,transparent 75%);}
@keyframes mcaOrb1{from{transform:translate3d(0,0,0) scale(1);}to{transform:translate3d(5vw,4vw,0) scale(1.15);}}
@keyframes mcaOrb2{from{transform:translate3d(0,0,0) scale(1.1);}to{transform:translate3d(-4vw,-3vw,0) scale(1);}}

@keyframes mcaFadeUp{from{opacity:0;transform:translateY(24px);}to{opacity:1;transform:none;}}
@keyframes mcaShine{to{background-position:200% center;}}
@keyframes mcaGlow{0%,100%{box-shadow:0 0 45px rgba(240,180,41,.22);}50%{box-shadow:0 0 90px rgba(240,180,41,.5);}}

section.main .stVerticalBlock > *{animation:mcaFadeUp .6s cubic-bezier(.22,1,.36,1) both;}
section.main .stVerticalBlock{gap:1.3rem;}
.block-container{max-width:1400px !important;width:100% !important;padding-left:2.4rem !important;padding-right:2.4rem !important;padding-top:2.2rem !important;}
@media (max-width:720px){.block-container{padding-left:1rem !important;padding-right:1rem !important;}}

.mca-hero-wrap{display:flex;align-items:center;justify-content:center;gap:46px;margin:20px auto 30px;animation:mcaFadeUp .9s cubic-bezier(.22,1,.36,1) both;}
.mca-logo{width:200px;height:200px;border-radius:50%;object-fit:cover;animation:mcaGlow 4.5s ease-in-out infinite;}
.mca-hero-fallback{font-size:100px;}
.mca-hero-box{border:1.5px solid transparent;border-radius:28px;padding:28px 52px;text-align:center;
background:linear-gradient(#0a0c12,#0a0c12) padding-box,
linear-gradient(115deg,rgba(240,180,41,.9),rgba(255,255,255,.15) 45%,rgba(240,180,41,.5)) border-box;
box-shadow:0 24px 80px rgba(0,0,0,.5);backdrop-filter:blur(8px);}
.mca-hero-badge{display:inline-block;padding:8px 18px;border-radius:999px;background:rgba(240,180,41,.12);
border:1px solid rgba(240,180,41,.45);color:#ffd166;font-size:12px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;margin-bottom:16px;}
.mca-hero-box h1{font-size:42px;margin:0;background:linear-gradient(90deg,#ffffff,#ffd97a 45%,#ffffff 90%);background-size:200%;
-webkit-background-clip:text;background-clip:text;color:transparent !important;animation:mcaShine 7s linear infinite;}
.mca-slogan{margin-top:12px;color:#f5c044;font-size:13px;letter-spacing:6px;text-transform:uppercase;font-weight:800;}

div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:22px !important;border:1px solid rgba(255,255,255,.10) !important;
background:linear-gradient(160deg,rgba(255,255,255,.07),rgba(255,255,255,.02) 60%) !important;
box-shadow:0 18px 60px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.08) !important;backdrop-filter:blur(12px);
transition:transform .35s cubic-bezier(.22,1,.36,1), border-color .3s ease, box-shadow .3s ease !important;}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-5px);border-color:rgba(240,180,41,.55) !important;
box-shadow:0 26px 80px rgba(240,167,27,.16), inset 0 1px 0 rgba(255,255,255,.12) !important;}

div.stButton>button, div.stButton>button p, div.stButton>button span,
div.stDownloadButton>button, div.stDownloadButton>button p{color:#181004 !important;font-weight:800 !important;}
div.stButton>button,div.stDownloadButton>button{border-radius:14px !important;border:none !important;padding:14px 26px !important;font-size:15px !important;
background:linear-gradient(135deg,#ffd166,#f0a71b 55%,#dd8f12) !important;
box-shadow:0 8px 26px rgba(240,167,27,.28), inset 0 1px 0 rgba(255,255,255,.5) !important;
transition:transform .22s ease,box-shadow .22s ease,filter .22s ease !important;}
div.stButton>button:hover,div.stDownloadButton>button:hover{transform:translateY(-2px);
box-shadow:0 14px 40px rgba(240,167,27,.5), inset 0 1px 0 rgba(255,255,255,.6) !important;filter:brightness(1.06);}
div.stButton>button:active{transform:translateY(0) scale(.99);}

div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input{
background:transparent !important;border:none !important;box-shadow:none !important;
outline:none !important;color:#eef1f6 !important;}
div[data-testid="stTextInput"] > div,div[data-testid="stTextArea"] > div,
div[data-testid="stSelectbox"] > div,div[data-testid="stNumberInput"] > div{
background:rgba(255,255,255,.06) !important;border:1px solid transparent !important;
border-radius:14px !important;transition:all .2s ease !important;}
div[data-testid="stTextInput"]:focus-within > div,div[data-testid="stTextArea"]:focus-within > div,
div[data-testid="stSelectbox"]:focus-within > div,div[data-testid="stNumberInput"]:focus-within > div{
border-color:rgba(240,180,41,.7) !important;background:rgba(255,255,255,.09) !important;}
input[type="radio"],input[type="checkbox"]{accent-color:#f0b429;}

div[data-testid="stExpander"]{border:1px solid rgba(255,255,255,.09) !important;border-radius:16px !important;background:rgba(255,255,255,.025) !important;}
div[data-testid="stExpander"] summary{font-weight:700;color:#e8ebf2;}
div[data-testid="stTabs"] button{color:#98a0ae;font-weight:700;border-radius:10px;}
div[data-testid="stTabs"] button:hover{color:#ffd166;background:rgba(240,180,41,.07);}
div[data-testid="stTabs"] button[aria-selected="true"]{color:#ffd166 !important;background:rgba(240,180,41,.10) !important;}
div[data-testid="stTabs"] > div{border-bottom:1px solid rgba(255,255,255,.08);}
div[data-testid="stMetric"]{background:linear-gradient(180deg,rgba(240,180,41,.10),rgba(240,180,41,.02)) !important;border:1px solid rgba(240,180,41,.3) !important;border-radius:18px !important;padding:14px 20px !important;}
div[data-testid="stMetric"] label{color:#ffd166 !important;}
div[data-testid="stError"],div[data-testid="stWarning"],div[data-testid="stSuccess"],div[data-testid="stInfo"]{border-radius:14px !important;}
blockquote{border-left:3px solid #f0b429 !important;background:rgba(240,180,41,.07) !important;border-radius:0 12px 12px 0 !important;padding:10px 18px !important;color:#d9dde6 !important;}
pre{border-radius:14px !important;border:1px solid rgba(255,255,255,.08) !important;}
div[data-testid="stProgress"] > div{background:rgba(255,255,255,.08) !important;border-radius:99px !important;}
div[data-testid="stPopover"] > div{border-radius:20px !important;overflow:hidden;background:rgba(11,14,20,.92) !important;
backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.12) !important;box-shadow:0 30px 90px rgba(0,0,0,.65) !important;}
div[data-testid="stPopover"] button{border-radius:0 !important;border:none !important;border-bottom:1px solid rgba(255,255,255,.05) !important;
background:transparent !important;color:#e8ebf2 !important;justify-content:flex-start !important;padding:13px 20px !important;font-weight:600 !important;}
div[data-testid="stPopover"] button:hover{background:rgba(240,180,41,.12) !important;color:#ffd166 !important;}

::-webkit-scrollbar{width:10px;height:10px;}
::-webkit-scrollbar-thumb{background:rgba(240,180,41,.35);border-radius:99px;}
::-webkit-scrollbar-track{background:transparent;}

/* ================= HOMEPAGE v8 ================= */
.mca-hero-sub{margin:6px auto 26px;font-size:18px;color:#c9ced9;max-width:680px;text-align:center;line-height:1.6;}
.mca-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:36px 0;}
.mca-stat{padding:22px 18px;text-align:center;border-radius:18px;position:relative;overflow:hidden;
background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.015));
border:1px solid rgba(255,255,255,.09);backdrop-filter:blur(8px);transition:all .3s ease;}
.mca-stat:hover{transform:translateY(-3px);border-color:rgba(240,180,41,.5);box-shadow:0 14px 40px rgba(240,167,27,.18);}
.mca-stat-value{font-family:'Unbounded',sans-serif;font-size:30px;font-weight:800;line-height:1;
background:linear-gradient(92deg,#ffd166,#fff);-webkit-background-clip:text;background-clip:text;color:transparent;}
.mca-stat-label{margin-top:6px;font-size:13px;color:#98a0ae;letter-spacing:.4px;text-transform:uppercase;}

.mca-step{position:relative;padding:28px 24px 24px;border-radius:22px;margin-bottom:16px;overflow:hidden;min-height:180px;
background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.01));
border:1px solid rgba(255,255,255,.10);backdrop-filter:blur(10px);transition:all .35s cubic-bezier(.22,1,.36,1);}
.mca-step:hover{transform:translateY(-6px);border-color:rgba(240,180,41,.55);box-shadow:0 24px 70px rgba(240,167,27,.2);}
.mca-step-num{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;
background:linear-gradient(135deg,#ffd166,#f0a71b);color:#181004;font-weight:800;font-size:18px;
box-shadow:0 6px 20px rgba(240,167,27,.4);margin-bottom:14px;}
.mca-step h3{font-size:18px !important;color:#fff !important;margin:0 0 10px 0 !important;}
.mca-step p{margin:0;color:#c9ced9;font-size:14.5px;line-height:1.55;}

.mca-doctype{padding:22px;border-radius:18px;margin-bottom:16px;min-height:130px;position:relative;overflow:hidden;
background:linear-gradient(160deg,rgba(255,255,255,.05),rgba(255,255,255,.01));
border:1px solid rgba(255,255,255,.09);backdrop-filter:blur(8px);transition:all .3s ease;}
.mca-doctype:hover{transform:translateY(-4px);border-color:rgba(240,180,41,.5);box-shadow:0 16px 50px rgba(240,167,27,.15);}
.mca-doctype-icon{font-size:28px;margin-bottom:8px;}
.mca-doctype h4{font-size:15px !important;color:#ffd166 !important;margin:0 0 6px 0 !important;font-weight:700;}
.mca-doctype p{margin:0;color:#b8bfcc;font-size:13.5px;line-height:1.5;}

.mca-benefit{padding:26px 22px;border-radius:20px;margin-bottom:16px;min-height:160px;position:relative;overflow:hidden;
background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.01));
border:1px solid rgba(255,255,255,.10);backdrop-filter:blur(10px);transition:all .35s ease;}
.mca-benefit:hover{transform:translateY(-5px);border-color:rgba(240,180,41,.55);box-shadow:0 20px 60px rgba(240,167,27,.18);}
.mca-benefit-icon{font-size:32px;margin-bottom:12px;display:inline-block;}
.mca-benefit h4{font-size:17px !important;color:#fff !important;margin:0 0 10px 0 !important;}
.mca-benefit p{margin:0;color:#c9ced9;font-size:14.5px;line-height:1.55;}

.mca-doctype::after,.mca-step::after,.mca-benefit::after,.mca-stat::after{content:"";position:absolute;top:0;left:-80%;
width:50%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.09),transparent);
transform:skewX(-20deg);transition:left .7s ease;pointer-events:none;}
.mca-doctype:hover::after,.mca-step:hover::after,.mca-benefit:hover::after,.mca-stat:hover::after{left:130%;}

.mca-review{padding:22px;border-radius:18px;margin-bottom:16px;min-height:140px;
background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.015));
border:1px solid rgba(255,255,255,.10);backdrop-filter:blur(8px);}
.mca-review-author{font-size:13px;color:#ffd166;font-weight:700;margin-bottom:8px;}
.mca-review > div:last-child{color:#c9ced9;font-size:14.5px;line-height:1.6;font-style:italic;}

.mca-faq{padding:20px 24px 20px 22px;margin-bottom:12px;border-radius:16px;border-left:3px solid rgba(240,180,41,.6);
background:linear-gradient(160deg,rgba(255,255,255,.05),rgba(255,255,255,.012));
border-top:1px solid rgba(255,255,255,.07);border-right:1px solid rgba(255,255,255,.07);border-bottom:1px solid rgba(255,255,255,.07);
transition:all .25s ease;position:relative;overflow:hidden;}
.mca-faq:hover{border-left-color:#ffd166;transform:translateX(3px);box-shadow:0 10px 34px rgba(240,167,27,.12);}
.mca-faq-q{font-weight:800;color:#ffd166;font-size:16px;margin-bottom:10px;font-family:'Unbounded',sans-serif;}
.mca-faq > div:last-child{color:#c9ced9;font-size:14.5px;line-height:1.65;}

.mca-section-head{text-align:center;margin:24px 0 8px;}
.mca-section-head h2{font-size:32px !important;margin:0 !important;
background:linear-gradient(92deg,#fff,#ffd97a 50%,#fff);background-size:200%;
-webkit-background-clip:text;background-clip:text;color:transparent;animation:mcaShine 9s linear infinite;}
.mca-section-head h2::after{display:none;}
.mca-section-head p{color:#98a0ae;font-size:15px;margin-top:10px;}

hr{border:none !important;height:1px !important;margin:40px 0 !important;
background:linear-gradient(90deg,transparent,rgba(240,180,41,.35),transparent) !important;}

@media (prefers-reduced-motion: reduce){*{animation:none !important;transition:none !important;}}
@media (max-width:720px){
  .mca-hero-wrap{flex-direction:column;gap:16px;margin:8px 8px 24px;}
  .mca-logo{width:112px;height:112px;}
  .mca-hero-fallback{font-size:64px;}
  .mca-hero-box{padding:18px 20px;border-radius:20px;width:100%;box-sizing:border-box;}
  .mca-hero-box h1{font-size:22px;}
  .mca-slogan{font-size:9px;letter-spacing:3px;}
  .mca-hero-sub{font-size:15px;}
  .mca-stats{grid-template-columns:repeat(2,1fr);}.mca-stat-value{font-size:22px;}
  div[data-testid="stHorizontalBlock"]{flex-direction:column !important;gap:12px !important;}
  div[data-testid="stHorizontalBlock"] > div{width:100% !important;}
  h1{font-size:24px !important;} h2{font-size:20px !important;} h3{font-size:17px !important;}
  .mca-section-head h2{font-size:24px !important;}
}
@media (min-width:721px) and (max-width:1024px){
  .mca-logo{width:150px;height:150px;}
  .mca-hero-box{padding:20px 28px;}
  .mca-hero-box h1{font-size:27px;}
}
.mca-support-bubble{position:fixed;bottom:24px;right:24px;z-index:99999;display:flex;align-items:center;gap:10px;
background:linear-gradient(135deg,#ffd166,#f0a71b);color:#181004 !important;text-decoration:none !important;
font-weight:800 !important;padding:14px 22px;border-radius:999px;font-size:15px;cursor:pointer;
box-shadow:0 12px 34px rgba(240,167,27,.5), inset 0 1px 0 rgba(255,255,255,.5);
transition:transform .22s ease, box-shadow .22s ease;animation:mcaFadeUp .8s .4s cubic-bezier(.22,1,.36,1) both;}
.mca-support-bubble svg{display:block;}
.mca-support-bubble:hover{transform:translateY(-4px) scale(1.04);box-shadow:0 18px 48px rgba(240,167,27,.65);color:#181004 !important;}
@media (max-width:720px){.mca-support-bubble{bottom:14px;right:14px;padding:12px 18px;font-size:14px;}}
</style>
"""