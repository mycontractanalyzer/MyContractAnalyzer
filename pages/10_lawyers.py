import streamlit as st

from core.records import save_consult_request
from core.ui import render_header
from utils.auth import get_current_user

st.set_page_config(page_title="Юристы", page_icon="🧑‍⚖️")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт, чтобы оставить заявку.")
    st.stop()

st.title("🧑‍⚖️ Маркетплейс юристов")
st.caption("Проверенные юристы-партнёры. Оставь заявку — юрист свяжется с тобой. Оплата после подтверждения.")

LAWYERS = [
    {"name": "Партнёр · Договорное право", "spec": "Аренда, услуги, подряд, трудовой",
     "price": "💬 Консультация в чате — 490 ₽", "time": "ответ до 24 часов"},
    {"name": "Партнёр · Корпоративное право", "spec": "ООО, учредительные договоры, бизнес-сделки",
     "price": "📞 Звонок 30 минут — 990 ₽", "time": "запись на удобное время"},
    {"name": "Партнёр · Недвижимость", "spec": "Покупка/аренда жилья, ДДУ, ипотека",
     "price": "📄 Разбор договора с правками — 1490 ₽", "time": "до 48 часов"},
]

for law in LAWYERS:
    with st.container(border=True):
        st.markdown(f"**{law['name']}**")
        st.write(f"Специализация: {law['spec']}")
        st.write(f"{law['price']} · {law['time']}")
        if st.button("📩 Оставить заявку", key=f"law_{law['name']}"):
            st.session_state[f"open_{law['name']}"] = True
        if st.session_state.get(f"open_{law['name']}"):
            q = st.text_area("Опиши задачу", key=f"q_{law['name']}")
            c = st.text_input("Telegram или телефон", key=f"c_{law['name']}")
            if st.button("Отправить", key=f"s_{law['name']}"):
                save_consult_request(user["id"], None, f"[МАРКЕТПЛЕЙС] {law['name']}: {q}", c)
                st.success("Заявка отправлена юристу!")