import os
import re

from fpdf import FPDF

FONT_REGULAR = [
    os.path.join(os.path.dirname(__file__), "..", "fonts", "arial.ttf"),
    "C:/Windows/Fonts/arial.ttf",
]
FONT_BOLD = [
    os.path.join(os.path.dirname(__file__), "..", "fonts", "arialbd.ttf"),
    "C:/Windows/Fonts/arialbd.ttf",
]

_ALLOWED = re.compile(r"[^A-Za-zА-Яа-яЁё0-9\s.,;:!?()%№+=/•·«»\"'—–-]")

KEYS = [
    ("красные флаги", (220, 50, 50), True),
    ("жёлтые флаги", (250, 190, 40), True),
    ("желтые флаги", (250, 190, 40), True),
    ("чек-лист", (60, 180, 80), True),
    ("краткий вывод", None, True),
    ("вопросы, которые стоит задать", None, True),
]


def _find(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def _clean(text: str) -> str:
    text = text.replace("**", "").replace("###", "").replace("##", "").replace("#", "")
    return _ALLOWED.sub("", text)


def _bullet(pdf, r, g, b):
    pdf.set_fill_color(r, g, b)
    pdf.circle(pdf.get_x() + 2, pdf.get_y() + 2.5, 1.6, "F")
    pdf.set_x(pdf.get_x() + 6)


def _render_line(pdf, family, has_bold, line):
    low = line.lower()
    bold_style = "B" if has_bold else ""

    pos, key, color, make_bold = -1, None, None, False
    for k, c, b in KEYS:
        i = low.find(k)
        if i != -1 and (pos == -1 or i < pos):
            pos, key, color, make_bold = i, k, c, b

    if key is None:
        pdf.set_font(family, "", 10)
        pdf.multi_cell(0, 6, line)
        return

    if color:
        _bullet(pdf, *color)

    rest_start = pos + len(key)
    while rest_start < len(line) and line[rest_start] in ":—-":
        rest_start += 1

    before = line[:pos]
    phrase = line[pos:rest_start]
    rest = line[rest_start:]

    pdf.set_font(family, "", 10)
    if before:
        pdf.write(6, before)
    pdf.set_font(family, bold_style if make_bold else "", 10)
    pdf.write(6, phrase)
    pdf.set_font(family, "", 10)
    pdf.write(6, rest)
    pdf.ln(6)


def generate_report_pdf(report: str, email: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    regular = _find(FONT_REGULAR)
    bold = _find(FONT_BOLD)
    family = "Arial" if regular else "Helvetica"
    if regular:
        pdf.add_font("Arial", "", regular)
    if bold:
        pdf.add_font("Arial", "B", bold)
    has_bold = (bold is not None) or (family == "Helvetica")

    pdf.add_page()
    pdf.set_font(family, "B" if has_bold else "", 14)
    pdf.multi_cell(0, 8, "MyContractAnalyzer — отчёт об анализе договора")
    pdf.ln(3)
    pdf.set_font(family, "", 10)
    pdf.multi_cell(0, 6, f"Пользователь: {email}")
    pdf.ln(4)

    for raw_line in _clean(report).split("\n"):
        line = raw_line.strip()
        if not line:
            pdf.ln(2)
            continue
        _render_line(pdf, family, has_bold, line)

    pdf.ln(6)
    pdf.set_draw_color(120, 120, 120)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    pdf.set_font(family, "", 8)
    pdf.multi_cell(0, 5, "* Документ сгенерирован автоматически и не является юридической консультацией.")

    return pdf.output()