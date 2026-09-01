import asyncio
import io
import re

import streamlit as st

_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U0000FE00-\U0000FE0F]"
)


@st.cache_data
def generate_audio(text: str) -> bytes:
    import edge_tts

    clean = _EMOJI.sub("", text or "").replace("**", "")[:6000]

    async def _run():
        comm = edge_tts.Communicate(clean, "ru-RU-DmitryNeural")
        buf = io.BytesIO()
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])
        return buf.getvalue()

    return asyncio.run(_run())
def generate_dialogue_audio(lines):
    import edge_tts

    async def _run():
        buf = io.BytesIO()
        for speaker, text in lines:
            voice = "ru-RU-DmitryNeural" if speaker == "A" else "ru-RU-SvetlanaNeural"
            comm = edge_tts.Communicate(_EMOJI.sub("", text).replace("**", "")[:400], voice)
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])
        return buf.getvalue()

    return asyncio.run(_run())