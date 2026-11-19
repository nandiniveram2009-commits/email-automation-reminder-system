import logging
from pathlib import Path
import pandas as pd


def load_and_merge_data(
    contacts_path: Path,
    reminders_path: Path,
    logger: logging.Logger,
) -> pd.DataFrame:
    """Load contacts and reminders CSVs, filter active entries, and merge on email."""
    if not contacts_path.exists():
        raise FileNotFoundError(f"Contacts file not found: {contacts_path}")
    if not reminders_path.exists():
        raise FileNotFoundError(f"Reminders file not found: {reminders_path}")

    contacts_df = pd.read_csv(contacts_path, dtype=str).fillna("N/A")
    reminders_df = pd.read_csv(reminders_path, dtype=str).fillna("N/A")

    # Normalize column names and key emails
    contacts_df.columns = contacts_df.columns.str.strip()
    reminders_df.columns = reminders_df.columns.str.strip()
    contacts_df["email"] = contacts_df["email"].str.strip().str.lower()
    reminders_df["email"] = reminders_df["email"].str.strip().str.lower()

    # Keep only active contacts and active reminders
    active_contacts = contacts_df[contacts_df["status"].str.lower() == "active"]
    active_reminders = reminders_df[reminders_df["active"].str.lower() == "yes"]

    merged = pd.merge(active_reminders, active_contacts, on="email", how="inner")

    skipped = len(active_reminders) - len(merged)
    if skipped > 0:
        logger.warning(
            f"Skipped {skipped} reminder(s) because the contact is inactive or missing."
        )

    logger.info(f"Loaded {len(merged)} active, eligible reminder(s) for processing.")
    return merged