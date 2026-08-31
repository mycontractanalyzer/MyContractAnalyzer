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


def generate_report_pdf(report: str, email: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font = _font_path()
    if font:
        pdf.add_font("mca", "", font)
        pdf.add_font("mca", "B", font)
        fam = "mca"
        prep = _clean
    else:
        fam = "Helvetica"
        prep = _latin

    pdf.set_font(fam, "B", 14)
    pdf.multi_cell(0, 8, prep("MyContractAnalyzer — отчёт по анализу договора"))
    pdf.set_font(fam, "", 9)
    pdf.multi_cell(0, 6, prep(f"Запрошен: {email} · Не является юридической консультацией"))
    pdf.ln(4)

    for line in (report or "").splitlines():
        line = line.rstrip()
        if not line.strip():
            pdf.ln(2)
            continue
        if line.startswith("### ") or line.startswith("## "):
            pdf.ln(2)
            pdf.set_font(fam, "B", 12)
            pdf.multi_cell(0, 7, prep(line.replace("#", "").replace("**", "").strip()))
            pdf.set_font(fam, "", 10)
        elif line.startswith("- "):
            pdf.multi_cell(0, 6, "• " + prep(line[2:]))
        else:
            pdf.multi_cell(0, 6, prep(line.replace("**", "")))

    return bytes(pdf.output())