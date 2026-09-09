(function(){
  var l = document.createElement('link');
  l.rel = 'icon';
  l.href = '/favicon.png?v=2';
  document.head.appendChild(l);
})();

var MCA_DEMO = 0; // сюда потом вставь номер публичного отчёта-примера (report.html?id=N). 0 = кнопка выключена

function mcaToken(){ return localStorage.getItem('mca_token'); }

function mcaEsc(t){ return (t || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function mcaMd(t){
  var h = mcaEsc(t);
  h = h.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
  h = h.replace(/^### (.*)$/gm,'<h4 class="font-bold text-lg mt-4 mb-1">$1</h4>');
  h = h.replace(/^## (.*)$/gm,'<h3 class="font-bold text-xl mt-5 mb-2">$1</h3>');
  h = h.replace(/^# (.*)$/gm,'<h2 class="font-bold text-2xl mt-6 mb-2">$1</h2>');
  return h.replace(/\n/g,'<br>');
}

async function mcaDownload(url, fname){
  var r = await fetch(url, {headers: {'Authorization': 'Bearer ' + mcaToken()}});
  if (!r.ok) { alert('Недоступно'); return; }
  var b = await r.blob();
  var a = document.createElement('a');
  a.href = URL.createObjectURL(b); a.download = fname; a.click();
  URL.revokeObjectURL(a.href);
}

function mcaNav(){
  var el = document.getElementById('siteNav');
  if (!el) return;
  var right = mcaToken()
    ? '<a href="/analyze.html" class="nav-link">Анализ</a>'
      + '<a href="/lawyer.html" class="nav-link">ИИ-юрист</a>'
      + '<a href="/profile.html" class="px-4 py-2 rounded-xl bg-amber-500 text-black font-semibold hover:bg-amber-400 transition">Кабинет</a>'
      + '<button onclick="localStorage.removeItem(\'mca_token\');location.href=\'/\'" class="nav-link">Выйти</button>'
    : (MCA_DEMO ? '<a href="/report.html?id=' + MCA_DEMO + '" class="nav-link">👀 Пример отчёта</a>' : '')
      + '<a href="/auth.html#login" class="nav-link">Войти</a>'
      + '<a href="/auth.html#signup" class="px-4 py-2 rounded-xl bg-amber-500 text-black font-semibold hover:bg-amber-400 transition">Регистрация</a>';
  el.innerHTML =
    '<nav class="sticky top-0 z-50 backdrop-blur-xl bg-[#0b0d12]/75 border-b border-white/5">'
    + '<div class="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between gap-4">'
    + '<a href="/" class="flex items-center gap-3 font-bold text-lg font-display min-w-0"><img src="/logo.png?v=2" class="logo-img" alt="⚖️"><span class="break-words">MyContractAnalyzer</span></a>'
    + '<div class="hidden lg:flex items-center gap-1 text-sm">'
    + '<a href="/#features" class="nav-link">Возможности</a>'
    + '<a href="/#how" class="nav-link">Как работает</a>'
    + '<a href="/#pricing" class="nav-link">Тарифы</a>'
    + '<a href="/#faq" class="nav-link">FAQ</a></div>'
    + '<div class="flex items-center gap-2 text-sm">' + right + '</div></div></nav>';
}

function mcaFooter(){
  var el = document.getElementById('siteFooter');
  if (!el) return;
  el.innerHTML =
    '<footer class="site mt-20">'
    + '<div class="max-w-6xl mx-auto px-6 py-10">'
    + '<div class="flex flex-wrap items-center gap-4 mb-5">'
    + '<img src="/logo.png?v=2" class="logo-img" alt="⚖️">'
    + '<span class="font-bold text-lg font-display">MyContractAnalyzer</span>'
    + '<span class="text-white/40 text-sm">· See what you\'re signing</span></div>'
    + '<p class="text-white/50 text-sm max-w-2xl mb-8">Сервис ИИ-анализа договоров. Результаты носят информационный характер и не являются юридической консультацией.</p>'
    + '<div class="grid gap-8 text-sm md:grid-cols-3">'
    + '<div class="f-col"><div class="font-bold mb-3 text-white">Продукт</div><a href="/analyze.html">Анализ договора</a><a href="/lawyer.html">ИИ-юрист 24/7</a><a href="/content.html">Знания и подкасты</a><a href="/#pricing">Тарифы</a></div>'
    + '<div class="f-col"><div class="font-bold mb-3 text-white">Документы</div><a href="/offer.html">Оферта</a><a href="/privacy.html">Политика конфиденциальности</a><a href="/consent.html">Согласие на обработку ПДн</a></div>'
    + '<div class="f-col"><div class="font-bold mb-3 text-white">Контакты</div><a href="/profile.html">Поддержка в кабинете</a><a href="mailto:support@mycontractanalyzer.ru">support@mycontractanalyzer.ru</a></div>'
    + '</div></div>'
    + '<div class="border-t border-white/5 py-6 text-center text-xs text-white/40">© 2026 MyContractAnalyzer</div></footer>';
}

function mcaReveal(){
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if (e.isIntersecting) e.target.classList.add('on'); });
  }, {threshold: .12});
  document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });
}