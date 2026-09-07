import streamlit as st

from core.feedback import list_feedbacks
from core.i18n import t
from core.pricing_ui import render_pricing
from core.ui import inject_style, render_hero, render_menu
from database.connection import ensure_schema
from database.models import init_db

init_db()
ensure_schema()

st.set_page_config(page_title="MyContractAnalyzer", page_icon="⚖️", layout="wide")

inject_style()
render_hero()
render_menu()

st.markdown(
    '<p class="mca-hero-sub">Нейросеть, обученная на юридических текстах, читает твой договор '
    "целиком и объясняет каждый риск простым языком. Подписывай уверенно — или требуй правок.</p>",
    unsafe_allow_html=True,
)
_, cta_col, _ = st.columns([1, 2, 1])
with cta_col:
    if st.button("🚀 Проверить договор", use_container_width=True, key="cta_top"):
        st.switch_page("pages/2_dashboard.py")

st.markdown(
    '<div class="mca-stats">'
    '<div class="mca-stat"><div class="mca-stat-value">0 ₽</div><div class="mca-stat-label">Первая проверка</div></div>'
    '<div class="mca-stat"><div class="mca-stat-value">24/7</div><div class="mca-stat-label">Доступ</div></div>'
    '<div class="mca-stat"><div class="mca-stat-value">РФ</div><div class="mca-stat-label">Данные в России</div></div>'
    '<div class="mca-stat"><div class="mca-stat-value">PDF</div><div class="mca-stat-label">Готовый отчёт</div></div>'
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="mca-section-head"><h2>Как это работает</h2>'
    "<p>Три простых шага от файла до готового отчёта</p></div>",
    unsafe_allow_html=True,
)
s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(
        '<div class="mca-step"><div class="mca-step-num">1</div>'
        "<h3>Загрузи договор</h3>"
        "<p>Текст, PDF или Word — любой формат. Загрузка занимает 5 секунд. "
        "Шифрованный канал, данные не уходят третьим лицам.</p></div>",
        unsafe_allow_html=True,
    )
with s2:
    st.markdown(
        '<div class="mca-step"><div class="mca-step-num">2</div>'
        "<h3>Получи риск-скор</h3>"
        "<p>AI оценит договор по 100-балльной шкале, найдёт скрытые риски "
        "и объяснит каждый из них простым языком.</p></div>",
        unsafe_allow_html=True,
    )
with s3:
    st.markdown(
        '<div class="mca-step"><div class="mca-step-num">3</div>'
        "<h3>Подписывай спокойно</h3>"
        "<p>Ты точно знаешь, на что соглашаешься. Скачай отчёт в PDF или Word, "
        "отправь контрагенту правки или покажи юристу.</p></div>",
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    '<div class="mca-section-head"><h2>Какие договоры анализируем</h2>'
    "<p>От аренды квартиры до сложных B2B-контрактов</p></div>",
    unsafe_allow_html=True,
)
types = [
    ("🏠", "Аренда квартиры", "Защита от внезапного выселения и скрытых платежей"),
    ("💼", "Трудовой договор", "Условия увольнения, отпуска, испытательного срока"),
    ("🤝", "Услуги и фриланс", "Сроки, оплата, права на результат работы"),
    ("🔐", "NDA", "Что нельзя разглашать и какие штрафы за разглашение"),
    ("💳", "Кредитный договор", "Скрытые комиссии, досрочное погашение"),
    ("📦", "Подряд и поставка", "Сроки поставки, неустойки, приёмка результата"),
]
for row in range(0, len(types), 3):
    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, types[row:row + 3]):
        with col:
            st.markdown(
                f'<div class="mca-doctype"><div class="mca-doctype-icon">{icon}</div>'
                f"<h4>{title}</h4><p>{desc}</p></div>",
                unsafe_allow_html=True,
            )

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    '<div class="mca-section-head"><h2>Что получает клиент</h2>'
    "<p>Три блока отчёта, которые говорят всё важное о твоём договоре</p></div>",
    unsafe_allow_html=True,
)
b1, b2, b3 = st.columns(3)
with b1:
    st.markdown(
        '<div class="mca-benefit"><div class="mca-benefit-icon">❗</div>'
        "<h4>Осторожно</h4>"
        "<p>Список опасных пунктов с номерами и объяснением, чем именно они грозят "
        "и как защититься.</p></div>",
        unsafe_allow_html=True,
    )
with b2:
    st.markdown(
        '<div class="mca-benefit"><div class="mca-benefit-icon">🟡</div>'
        "<h4>Следует уточнить</h4>"
        "<p>Что обсудить со второй стороной перед подписанием, "
        "чтобы избежать будущих споров.</p></div>",
        unsafe_allow_html=True,
    )
with b3:
    st.markdown(
        '<div class="mca-benefit"><div class="mca-benefit-icon">✅</div>'
        "<h4>Чек-лист</h4>"
        "<p>Финальный список: что обязательно проверить перед тем, "
        "как ставить подпись.</p></div>",
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    '<div class="mca-section-head"><h2>Отзывы пользователей</h2>'
    "<p>Что говорят те, кто уже проверил свои договоры</p></div>",
    unsafe_allow_html=True,
)
fbs = list_feedbacks(50)
positive = [f for f in fbs if f["rating"] >= 4 and (f["comment"] or "").strip()]
if not positive:
    st.info("Пока нет отзывов с комментариями — будьте первым!")
else:
    cols = st.columns(min(3, len(positive)))
    for col, f in zip(cols, positive[:3]):
        with col:
            st.markdown(
                f'<div class="mca-review">'
                f'<div class="mca-review-author">⭐ {f["email"] or "Пользователь"}</div>'
                f'<div>{f["comment"]}</div></div>',
                unsafe_allow_html=True,
            )

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    '<div class="mca-section-head"><h2>Частые вопросы</h2>'
    "<p>Всё, что вы хотели знать перед началом работы</p></div>",
    unsafe_allow_html=True,
)
faq = [
    ("Это действительно работает?",
     "Да. Мы используем современную нейросеть, специально настроенную на юридические тексты. "
     "Модель читает весь договор, а не выдёргивает ключевые слова."),
    ("Заменит ли это живого юриста?",
     "Для большинства типовых договоров — вполне заменяет первичную проверку. "
     "Для крупных сделок с высокими рисками рекомендуем дополнительно показать отчёт юристу."),
    ("Что происходит с моим документом?",
     "Текст обрабатывается в защищённом канале связи и хранится в зашифрованной базе. "
     "Мы не передаём данные третьим лицам. В любой момент можно удалить аккаунт со всеми данными."),
    ("Можно ли вернуть деньги за подписку?",
     "Если вы не воспользовались проверками — напишите нам в поддержку, "
     "разберёмся индивидуально."),
    ("Что делать, если нейросеть ошиблась?",
     "Нажми 👎 под отчётом и оставь комментарий — мы правим промпт по каждому такому случаю. "
     "Качество растёт с каждым отзывом."),
]
for q, a in faq:
    st.markdown(
        f'<div class="mca-faq"><div class="mca-faq-q">❓ {q}</div><div>{a}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    f'<div class="mca-section-head"><h2>{t("pricing")}</h2>'
    "<p>Выбери тариф под свою задачу</p></div>",
    unsafe_allow_html=True,
)
render_pricing()

st.markdown("<hr>", unsafe_allow_html=True)

_, cta_col2, _ = st.columns([1, 2, 1])
with cta_col2:
    if st.button("🚀 Начать сейчас — бесплатно", use_container_width=True, key="cta_bottom"):
        st.switch_page("pages/2_dashboard.py")