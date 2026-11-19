import logging
import time
from datetime import datetime
from typing import Dict, List
import schedule

from src.config import (
    CONTACTS_FILE,
    REMINDERS_FILE,
    TEMPLATES_DIR,
    OUTPUTS_DIR,
    SENDER_NAME,
)
from src.data_loader import load_and_merge_data
from src.template_engine import render_email_template
from src.mailer import send_or_simulate_email
from src.report_generator import save_execution_report


def process_reminders(dry_run: bool, logger: logging.Logger) -> List[Dict[str, str]]:
    """Execute one full pass of active reminders and return status records."""
    logger.info("=== Starting Reminder Processing Cycle ===")
    merged_df = load_and_merge_data(CONTACTS_FILE, REMINDERS_FILE, logger)
    results: List[Dict[str, str]] = []

    for _, row in merged_df.iterrows():
        context = {
            "name": row["name"],
            "email": row["email"],
            "department": row["department"],
            "company": row["company"],
            "event_title": row["event_title"],
            "due_date": row["due_date"],
            "schedule_time": row["schedule_time"],
            "amount": row["amount"],
            "sender_name": SENDER_NAME,
        }

        try:
            subject, body = render_email_template(
                TEMPLATES_DIR, row["template_name"], context
            )
            delivery = send_or_simulate_email(
                recipient_email=row["email"],
                subject=subject,
                body=body,
                dry_run=dry_run,
                logger=logger,
            )
        except Exception as exc:
            logger.error(
                f"[ERROR] Reminder {row['reminder_id']} ({row['email']}): {exc}"
            )
            subject = "TEMPLATE_ERROR"
            delivery = {"status": "FAILED", "error": str(exc)}

        results.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reminder_id": row["reminder_id"],
                "recipient_name": row["name"],
                "recipient_email": row["email"],
                "reminder_type": row["reminder_type"],
                "frequency": row["frequency"],
                "subject": subject,
                "mode": "DRY_RUN" if dry_run else "LIVE_SMTP",
                "status": delivery["status"],
                "error_message": delivery["error"],
            }
        )

    if results:
        save_execution_report(results, OUTPUTS_DIR, logger)
    else:
        logger.warning("No eligible reminders found to process.")

    logger.info("=== Reminder Processing Cycle Complete ===")
    return results


def run_scheduler(dry_run: bool, interval_seconds: int, logger: logging.Logger) -> None:
    """Run automated reminders continuously on a local schedule."""
    logger.info(
        f"Scheduler started (interval={interval_seconds}s, dry_run={dry_run}). Press Ctrl+C to stop."
    )

    # Run immediately once, then schedule recurring passes
    process_reminders(dry_run=dry_run, logger=logger)
    schedule.every(interval_seconds).seconds.do(
        process_reminders, dry_run=dry_run, logger=logger
    )

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped gracefully by user (Ctrl+C).")