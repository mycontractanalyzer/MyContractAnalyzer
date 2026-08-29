import streamlit as st

from core.analyzer import choose_model
from core.diff import diff_texts, summarize_diff
from core.prompts import build_compare_system_prompt
from core.ui import render_header
from integrations.deepseek import ask_deepseek
from utils.auth import get_current_user
from utils.file_io import read_uploaded_text

st.set_page_config(page_title="Сравнение версий", page_icon="🆚")
render_header()

user = get_current_user()
if not user:
    st.warning("Войди в аккаунт.")
    st.stop()

st.title("🆚 Сравнение версий договора")
st.caption(
    "Загрузи две версии: старую (которую уже смотрел) и новую. "
    "Мы покажем изменения и попросим ИИ объяснить, стало ли лучше."
)

c1, c2 = st.columns(2)
with c1:
    f1 = st.file_uploader("Старая версия", type=["pdf", "docx", "txt"], key="cmp_old")
with c2:
    f2 = st.file_uploader("Новая версия", type=["pdf", "docx", "txt"], key="cmp_new")

if st.button("🔍 Сравнить", disabled=not (f1 and f2)):
    old_text = read_uploaded_text(f1)
    new_text = read_uploaded_text(f2)

    st.subheader("📊 Статистика изменений")
    st.info(summarize_diff(old_text, new_text))

    st.subheader("🧠 Что говорит ИИ")
    with st.spinner("Анализирую различия..."):
        sys = build_compare_system_prompt(old_text, new_text)
        report = ask_deepseek(sys, "Сравни эти две версии договора.", choose_model(user["tariff"]))
    st.markdown(report)

    with st.expander("Показать технический diff"):
        st.code(diff_texts(old_text, new_text), language="diff")