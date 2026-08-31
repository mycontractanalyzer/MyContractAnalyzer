import os
import re

import requests
import streamlit as st
from fpdf import FPDF

FONT_URLS = [
    "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/ptsans/PT_Sans-Web-Regular.ttf",
    "https://cdn.jsdelivr.net/gh/dejavu-fonts/dejavu@master/ttf/DejaVuSans.ttf",
]

_EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-⬀-️←-]")


def _clean(s: str) -> str:
    return _EMOJI.sub("", s or "")


@st.cache_resource
def _font_path():
    for i, url in enumerate(FONT_URLS):
        try:
            r = requests.get(url, timeout=25)
            if r.ok and len(r.content) > 10000:
                p = f"/tmp/mca_font_{i}.ttf"
                if not os.path.exists(p):
                    with open(p, "wb") as f:
                        f.write(r.content)
                return p
        except Exception:
            continue
    return None


def _latin(s: str) -> str:
    return (s or "").encode("latin-1", "replace").decode("latin-1")


def _para(pdf, fam, style, size, text, lh=6):
    """Безопасный вывод абзаца: никогда не роняет генератор."""
    pdf.set_font(fam, style, size)
    pdf.set_x(pdf.l_margin)
    try:
        pdf.multi_cell(0, lh, text)
    except Exception:
        try:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, lh, text.encode("ascii", "ignore").decode())
        except Exception:
            pdf.set_x(pdf.l_margin)


def generate_report_pdf(report: str, email: str) -> bytes:
    pdf = FPDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font = _font_path()
    if font:
        pdf.add_font("mca", "", font)
        pdf.add_font("mca", "B", font)
        fam, prep = "mca", _clean
    else:
        fam, prep = "Helvetica", _latin

    _para(pdf, fam, "B", 14, prep("MyContractAnalyzer — отчёт по анализу договора"), 8)
    _para(pdf, fam, "", 9, prep(f"Запрошен: {email} · Не является юридической консультацией"))
    pdf.ln(3)

    for line in (report or "").splitlines():
        line = line.rstrip()
        if not line.strip():
            pdf.ln(2)
            continue
        if line.startswith("### ") or line.startswith("## "):
            pdf.ln(2)
            _para(pdf, fam, "B", 12, prep(line.replace("#", "").replace("**", "").strip()), 7)
        elif line.startswith("- "):
            _para(pdf, fam, "", 10, "• " + prep(line[2:]))
        else:
            _para(pdf, fam, "", 10, prep(line.replace("**", "")))

    return bytes(pdf.output())