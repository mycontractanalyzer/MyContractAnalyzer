(function(){
  var l = document.createElement('link');
  l.rel = 'icon';
  l.href = '/favicon.png?v=3';
  document.head.appendChild(l);
})();

var MCA_DEMO = 0; // сюда потом вставь номер публичного отчёта-примера (report.html?id=N). 0 = кнопка выключена

function mcaToken(){ return localStorage.getItem('mca_token'); }

function mcaEsc(t){ return (t || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function mcaMd(t){
  var h = mcaEsc(t);
  h = h.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
  h = h.replace(/\*(.+?)\*/g,'<i>$1</i>');
  h = h.replace(/^#### (.*)$/gm,'<h5 class="font-bold text-base mt-3 mb-1">$1</h5>');
  h = h.replace(/^### (.*)$/gm,'<h4 class="font-bold text-lg mt-4 mb-1">$1</h4>');
  h = h.replace(/^## (.*)$/gm,'<h3 class="font-bold text-xl mt-5 mb-2">$1</h3>');
  h = h.replace(/^# (.*)$/gm,'<h2 class="font-bold text-2xl mt-6 mb-2">$1</h2>');
  h = h.replace(/^---+$/gm,'<hr class="border-white/10 my-4">');
  h = h.replace(/^[-•] (.*)$/gm,'<span class="block pl-4">• $1</span>');
  h = h.replace(/((?:^[^\n|]*\|[^\n]*$(?:\n|$))+)/gm, function(block){
    var rows = block.trim().split('\n').filter(function(r){
      return r.indexOf('|') >= 0 && !/^\s*:?-{2,}.*:?-{2,}[\s|:-]*$/.test(r) && !/^\|[\s|:-]+\|$/.test(r.trim());
    });
    if (rows.length < 2) return block;
    var html = '<table class="w-full text-sm my-3 border-collapse">';
    rows.forEach(function(r, idx){
      var cells = r.split('|').map(function(c){ return c.trim(); });
      if (cells[0] === '') cells.shift();
      if (cells[cells.length - 1] === '') cells.pop();
      var tag = idx === 0 ? 'th' : 'td';
      html += '<tr>' + cells.map(function(c){ return '<' + tag + ' class="border border-white/10 px-2 py-1 text-left">' + c + '</' + tag + '>'; }).join('') + '</tr>';
    });
    return html + '</table>';
  });
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
    ? '<a href="/analyze.html" class="nav-link">Анализ</a><a href="/compare.html" class="nav-link">Сравнение</a>'
      + '<a href="/lawyer.html" class="nav-link">ИИ-юрист</a>'
      + '<a href="/profile.html" class="px-4 py-2 rounded-xl bg-amber-500 text-black font-semibold hover:bg-amber-400 transition">Кабинет</a>'
      + '<button onclick="localStorage.removeItem(\'mca_token\');location.href=\'/\'" class="nav-link">Выйти</button>'
    : (MCA_DEMO ? '<a href="/report.html?id=' + MCA_DEMO + '" class="nav-link">👀 Пример отчёта</a>' : '')
      + '<a href="/auth.html#login" class="nav-link">Войти</a>'
      + '<a href="/auth.html#signup" class="px-4 py-2 rounded-xl bg-amber-500 text-black font-semibold hover:bg-amber-400 transition">Регистрация</a>';
  el.innerHTML =
    '<nav class="sticky top-0 z-50 backdrop-blur-xl bg-[#0b0d12]/75 border-b border-white/5">'
+ '<div class="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between gap-6">'
    + '<a href="/" class="flex items-center gap-3 font-bold text-lg font-display shrink-0"><img src="/favicon.png?v=3" class="logo-img" alt="⚖️"><span class="hidden md:inline">MyContractAnalyzer</span></a>'
+ '<div class="hidden xl:flex items-center gap-2 text-sm">'
    + '<a href="/#features" class="nav-link">Возможности</a>'
    + '<a href="/#how" class="nav-link">Как работает</a>'
    + '<a href="/#pricing" class="nav-link">Тарифы</a>'
    + '<a href="/#faq" class="nav-link">FAQ</a></div>'
    + '<div class="nav-scroll flex items-center gap-2 text-sm max-lg:overflow-x-auto max-lg:max-w-[62vw]" style="-webkit-overflow-scrolling:touch">' + right + '</div></div></nav>';
}

function mcaFooter(){
  var el = document.getElementById('siteFooter');
  if (!el) return;
  el.innerHTML =
    '<footer class="site mt-20">'
    + '<div class="max-w-6xl mx-auto px-6 py-10">'
    + '<div class="flex flex-wrap items-center gap-4 mb-5">'
    + '<img src="/favicon.png?v=3" class="logo-img" alt="⚖️">'
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


function mcaPrompt(title, placeholder, def){
  return new Promise(resolve => {
    const wrap = document.createElement('div');
    wrap.className = 'fixed inset-0 z-[100] flex items-center justify-center px-4';
    wrap.style.cssText = 'background:rgba(0,0,0,.7);backdrop-filter:blur(6px)';
    wrap.innerHTML = '<div class="glass p-8 max-w-md w-full border-amber-500/30">' +
      '<h3 class="font-bold text-lg mb-4">' + title + '</h3>' +
      '<input id="mcaPromptInput" class="input" placeholder="' + (placeholder || '') + '" value="' + (def || '') + '">' +
      '<div class="flex gap-3 mt-6"><button id="mcaPromptOk" class="btn-primary flex-1 text-sm">Продолжить</button>' +
      '<button id="mcaPromptNo" class="btn-ghost flex-1 text-sm">Отмена</button></div></div>';
    document.body.appendChild(wrap);
    const done = v => { wrap.remove(); resolve(v); };
    wrap.querySelector('#mcaPromptOk').onclick = () => done(wrap.querySelector('#mcaPromptInput').value.trim() || null);
    wrap.querySelector('#mcaPromptNo').onclick = () => done(null);
    wrap.addEventListener('click', e => { if (e.target === wrap) done(null); });
    setTimeout(() => wrap.querySelector('#mcaPromptInput').focus(), 50);
  });
}


function mcaConfirm(title, text, yesLabel){
  return new Promise(resolve => {
    const wrap = document.createElement('div');
    wrap.className = 'fixed inset-0 z-[100] flex items-center justify-center px-4';
    wrap.style.cssText = 'background:rgba(0,0,0,.7);backdrop-filter:blur(6px)';
    wrap.innerHTML = '<div class="glass p-8 max-w-md w-full border-red-500/40">' +
      '<div class="text-4xl mb-4">🗑</div>' +
      '<h3 class="font-bold text-xl mb-3">' + title + '</h3>' +
      '<p class="text-sm text-white/60 mb-6">' + text + '</p>' +
      '<div class="flex gap-3"><button id="mcaCYes" class="btn-primary flex-1 text-sm" style="background:linear-gradient(135deg,#f87171,#dc2626);color:#fff;box-shadow:0 10px 30px rgba(220,38,38,.35)">' + (yesLabel || 'Да, удалить') + '</button>' +
      '<button id="mcaCNo" class="btn-ghost flex-1 text-sm">Отмена</button></div></div>';
    document.body.appendChild(wrap);
    const done = v => { wrap.remove(); resolve(v); };
    wrap.querySelector('#mcaCYes').onclick = () => done(true);
    wrap.querySelector('#mcaCNo').onclick = () => done(false);
    wrap.addEventListener('click', e => { if (e.target === wrap) done(false); });
  });
}