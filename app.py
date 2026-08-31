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
    "<style>div.stButton > button {padding: 18px 34px !important; font-size: 20px !important;}</style>",
    unsafe_allow_html=True,
)
_, cta_col, _ = st.columns([1, 2, 1])
with cta_col:
    st.page_link("pages/2_dashboard.py", label="🚀 Анализировать договор", use_container_width=True)

st.divider()

st.subheader("Как это работает")
c1, c2, c3 = st.columns(3)
with c1:
    st.header("1️⃣ Загрузи договор")
    st.write("Текст, PDF или Word — любой формат. Загрузка занимает 5 секунд.")
with c2:
    st.header("2️⃣ Получи риск-скор")
    st.write("AI за минуту оценит договор по 100-балльной шкале и объяснит каждый риск.")
with c3:
    st.header("3️⃣ Подписывай спокойно")
    st.write("Ты знаешь, на что соглашаешься. Скачай отчёт в PDF или Word.")

st.divider()

st.subheader("Какие договоры анализируем")
types = [
    ("🏠 Аренда квартиры", "Защита от внезапного выселения и скрытых платежей"),
    ("💼 Трудовой договор", "Проверка условий увольнения, отпуска, испытательного срока"),
    ("🤝 Услуги и фриланс", "Сроки, оплата, права на результат работы"),
    ("🔐 NDA", "Что нельзя разглашать и какие штрафы за разглашение"),
    ("💳 Кредитный договор", "Скрытые комиссии, порядок досрочного погашения"),
    ("📦 Подряд и поставка", "Сроки поставки, неустойки, приёмка результата"),
]
for row in range(0, len(types), 3):
    cols = st.columns(3)
    for col, (title, desc) in zip(cols, types[row:row + 3]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(desc)

st.divider()

st.subheader("Что получает клиент")
b1, b2, b3 = st.columns(3)
with b1:
    st.write("**❗ Осторожно**")
    st.write("Список опасных пунктов с номерами и объяснением, чем они грозят.")
with b2:
    st.write("**🟡 Следует уточнить**")
    st.write("Что обсудить со второй стороной перед подписанием.")
with b3:
    st.write("**✅ Чек-лист**")
    st.write("Что обязательно проверить перед тем, как ставить подпись.")

st.divider()

st.subheader("Отзывы пользователей")
fbs = list_feedbacks(50)
positive = [f for f in fbs if f["rating"] == 1 and (f["comment"] or "").strip()]
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

st.divider()

st.subheader("Частые вопросы")
faq = [
    ("Это действительно работает?", "Да. Мы используем современную нейросеть, специально настроенную на юридические тексты. Модель читает весь договор, а не выдёргивает ключевые слова."),
    ("Заменит ли это живого юриста?", "Для большинства типовых договоров — вполне заменяет первичную проверку. Для крупных сделок с высокими рисками рекомендуем дополнительно показать отчёт юристу."),
    ("Что происходит с моим документом?", "Текст обрабатывается в защищённом канале связи и хранится в зашифрованной базе. Мы не передаём данные третьим лицам. В любой момент можно удалить аккаунт со всеми данными."),
    ("Можно ли вернуть деньги за подписку?", "Если вы не воспользовались проверками — напишите нам в поддержку, разберёмся индивидуально."),
    ("Что делать, если нейросеть ошиблась?", "Нажми 👎 под отчётом и оставь комментарий — мы правим промпт по каждому такому случаю. Качество растёт с каждым отзывом."),
]
for q, a in faq:
    st.markdown(f'<div class="mca-faq"><div class="mca-faq-q">❓ {q}</div><div>{a}</div></div>', unsafe_allow_html=True)

st.divider()

st.subheader(t("pricing"))
render_pricing()

st.divider()
_, cta_col2, _ = st.columns([1, 2, 1])
with cta_col2:
    st.page_link("pages/2_dashboard.py", label="🚀 Начать сейчас", use_container_width=True)