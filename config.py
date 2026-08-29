import os

import streamlit as st


def _secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name)
        if value is not None:
            return str(value)
    except Exception:
        pass
    return os.environ.get(name, default)


DEEPSEEK_API_KEY = _secret("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = _secret("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

MODEL_FREE = _secret("MODEL_FREE", "deepseek-v4-flash")
MODEL_PAID = _secret("MODEL_PAID", "deepseek-v4-pro")

BIG_DOC_CHARS = 100_000

ADMIN_EMAILS = [e.strip().lower() for e in _secret("ADMIN_EMAILS", "admin@example.com").split(",") if e.strip()]