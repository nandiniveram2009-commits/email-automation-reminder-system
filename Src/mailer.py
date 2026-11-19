import logging
import smtplib
from email.message import EmailMessage
from typing import Dict

from src.config import SMTP_HOST, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, SENDER_NAME


def send_or_simulate_email(
    recipient_email: str,
    subject: str,
    body: str,
    dry_run: bool,
    logger: logging.Logger,
) -> Dict[str, str]:
    """Send an email via SMTP TLS or simulate delivery in Dry-Run mode."""
    if dry_run:
        logger.info(f"[DRY-RUN] Simulated email to {recipient_email} | Subject: '{subject}'")
        return {
            "status": "SIMULATED",
            "error": "",
        }

    if not SENDER_PASSWORD or "your_16_char" in SENDER_PASSWORD:
        error_msg = "Missing valid SENDER_PASSWORD in .env for live SMTP mode."
        logger.error(f"[FAILED] {recipient_email} | {error_msg}")
        return {"status": "FAILED", "error": error_msg}

    msg = EmailMessage()
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        logger.info(f"[SENT] Email delivered to {recipient_email} | Subject: '{subject}'")
        return {"status": "SENT", "error": ""}

    except smtplib.SMTPAuthenticationError:
        err = "SMTP authentication failed. Check SENDER_EMAIL and Gmail App Password."
        logger.error(f"[FAILED] {recipient_email} | {err}")
        return {"status": "FAILED", "error": err}
    except Exception as exc:
        err = str(exc)
        logger.error(f"[FAILED] {recipient_email} | {err}")
        return {"status": "FAILED", "error": err}