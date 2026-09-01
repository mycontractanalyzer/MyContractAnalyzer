import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st


def send_report_email(to_email: str, pdf_bytes: bytes, title: str) -> bool:
    sender = st.secrets.get("GMAIL_EMAIL")
    password = st.secrets.get("GMAIL_APP_PASSWORD")
    if not sender or not password:
        return False

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = f"MyContractAnalyzer — отчёт: {title}"
    msg.attach(MIMEText(
        "Здравствуйте!\n\nВо вложении — отчёт по анализу вашего договора.\n"
        "MyContractAnalyzer — See what you're signing.", "plain", "utf-8"))

    part = MIMEBase("application", "pdf")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", 'attachment; filename="report.pdf"')
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
        server.login(sender, password)
        server.sendmail(sender, [to_email], msg.as_string())
    return True