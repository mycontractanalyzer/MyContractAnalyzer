import base64

import requests
import streamlit as st

import config


def _key():
    return getattr(config, "DEEPSEEK_API_KEY", None) or st.secrets.get("DEEPSEEK_API_KEY")


def ocr_image(file_bytes, mime="image/jpeg"):
    b64 = base64.b64encode(file_bytes).decode()
    r = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {_key()}"},
        json={
            "model": "deepseek-v4-flash-vision-exp",
            "messages": [{"role": "user", "content": [
                {"type": "text",
                 "text": "Распознай ВЕСЬ текст с фотографии дословно, сохранив структуру и нумерацию. Верни только текст."},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ]}],
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]