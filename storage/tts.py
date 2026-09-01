import asyncio
import io
import re

import streamlit as st

_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_URL = re.compile(r"https?://\S+")
_ALLOWED = re.compile(r"[^\w\s.,!?;:()«»\"\"''\-—–%₽$€°№/]", re.UNICODE)


def _clean(text: str) -> str:
    s = text or ""
    s = _LINK.sub(r"\1", s)
    s = _URL.sub(" ", s)
    s = _ALLOWED.sub(" ", s)
    s = s.replace("_", " ")
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _comm(edge_tts, text, voice):
    try:
        return edge_tts.Communicate(text, voice, volume="-20%")
    except TypeError:
        return edge_tts.Communicate(text, voice)


def generate_audio(text: str) -> bytes:
    import edge_tts

    clean = _clean(text)[:6000]

    async def _run():
        comm = _comm(edge_tts, clean, "ru-RU-DmitryNeural")
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
            comm = _comm(edge_tts, _clean(text)[:400], voice)
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])
        return buf.getvalue()

    return asyncio.run(_run())