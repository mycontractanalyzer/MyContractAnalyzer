import streamlit as st

from core.i18n import t
from core.pricing_ui import render_pricing
from core.ui import render_header

from core.ui import render_header

render_header()

st.title(t("pricing"))
render_pricing()