import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from loggin import log_error, log_info

load_dotenv(".env")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


if (not EMAIL_USER or not EMAIL_PASSWORD):
    log_error("Missing email service environment variables.")
    raise ValueError(
        "EMAIL_USER and EMAIL_PASSWORD must be set in environment variables.")


def send_email(subject: str, body: str, to: str):
    global EMAIL_USER, EMAIL_PASSWORD

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to
    try:
        assert EMAIL_USER is not None and EMAIL_PASSWORD is not None, "Email credentials not configured"
        log_info(f"Sending email to {to} with subject '{subject}'")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
            log_info("Email sent successfully")
    except Exception as e:
        log_error(f"Error sending email: {e}")
