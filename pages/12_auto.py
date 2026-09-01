import streamlit as st

from core.extra_ai import analyze_policy
from core.ui import render_header
from utils.auth import get_current_user

st.set_page_config(page_title="Мир Автовладельца", page_icon="🚗")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

st.title("🚗 Мир Автовладельца")
st.caption("Всё для водителя в одном модуле: страховки, ДТП, ТО и проверка автодоговоров.")

tab1, tab2, tab3, tab4 = st.tabs(["🛡 Проверка полиса", "📋 Чек-лист ДТП", "🔧 ТО и платежи", "📄 Автодоговор"])

with tab1:
    policy = st.text_area("Вставь условия полиса (ОСАГО/КАСКО)", height=200)
    if st.button("🛡 Проверить полис"):
        with st.spinner("Анализирую полис..."):
            st.session_state["policy_report"] = analyze_policy(policy, user["tariff"])
    if st.session_state.get("policy_report"):
        st.markdown(st.session_state["policy_report"])

with tab2:
    ACCIDENT = [
        "Не уезжай с места, включи аварийку и выставь знак",
        "Сфотографируй место, оба авто со всех сторон, номера, повреждения",
        "Проверь полис ОСАГО второго водителя через приложение РСА",
        "Европротокол — если ущерб до лимита и нет спора о вине, иначе — ГИБДД",
        "Запиши контакты свидетелей",
        "Уведоми свою страховую в течение 5 рабочих дней",
        "Не подписывай пустые бланки и документы с прочерками",
    ]
    for i, step in enumerate(ACCIDENT, 1):
        st.checkbox(f"{i}. {step}", key=f"acc_{i}")

with tab3:
    mileage = st.number_input("Текущий пробег, км", min_value=0, value=50000, step=500)
    last_oil = st.number_input("Пробег при последней замене масла, км", min_value=0, value=45000, step=500)
    left = 15000 - (mileage - last_oil)
    if left > 0:
        st.success(f"До замены масла осталось примерно {left} км")
    else:
        st.error("ТО просрочено — запишись на сервис!")
    st.caption("Не забывай: ОСАГО — продление ежегодно; техосмотр — по актуальным правилам для твоего типа ТС.")

with tab4:
    st.info("Договор аренды авто (как Делика), купли-продажи или сервиса проверяется в основном анализе.")
    st.page_link("pages/2_dashboard.py", label="📄 Проверить автодоговор", use_container_width=True)