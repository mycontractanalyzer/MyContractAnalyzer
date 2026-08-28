import streamlit as st

from core.tariffs import DISPLAY_NAMES, FEATURES, PERIOD_DISCOUNTS, TARIFFS, price_for

MONTH_LABEL = {
    1: "за 1 месяц",
    3: "за 3 месяца",
    6: "за 6 месяцев",
    9: "за 9 месяцев",
    12: "за 12 месяцев",
    24: "за 24 месяца",
}


def render_pricing():
    months = st.selectbox(
        "Срок подписки",
        [1, 3, 6, 9, 12, 24],
        format_func=lambda m: f"{m} мес" + (f" (−{int(PERIOD_DISCOUNTS[m]*100)}%)" if PERIOD_DISCOUNTS[m] else ""),
    )

    names = list(TARIFFS.keys())
    for row_start in range(0, len(names), 3):
        cols = st.columns(3)
        for col, name in zip(cols, names[row_start:row_start + 3]):
            tdata = TARIFFS[name]
            with col:
                with st.container(border=True):
                    st.header(DISPLAY_NAMES.get(name, name))
                    if name == "Free":
                        st.write("**0 ₽** — навсегда")
                        st.write("• 1 пробная проверка")
                    else:
                        total = price_for(name, months)
                        st.write(f"**{total} ₽** {MONTH_LABEL[months]}")
                        st.caption(
                            f"≈ {round(total / months)} ₽/мес"
                            + (" с учётом скидки" if PERIOD_DISCOUNTS[months] else "")
                        )
                        st.write(f"• {tdata['checks']} проверок")
                    st.write(f"• Документы до {tdata['limit_chars'] // 1000} тыс. символов")
                    for f in FEATURES[name]:
                        st.write(f"• {f}")
        st.divider()