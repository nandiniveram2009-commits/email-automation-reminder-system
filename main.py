import argparse
from src.logger_setup import setup_logger
from src.scheduler_runner import process_reminders, run_scheduler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Email Automation & Reminder System"
    )
    parser.add_argument(
        "--mode",
        choices=["once", "schedule"],
        default="once",
        help="Run 'once' immediately or 'schedule' continuously (default: once).",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Interval in seconds for 'schedule' mode (default: 30).",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Send real emails via SMTP. Omit this flag to run safely in Dry-Run mode.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = setup_logger()
    dry_run = not args.live

    logger.info(
        f"Launching Email Automation System | Mode: {args.mode.upper()} | "
        f"Mode Type: {'DRY-RUN (Safe Simulation)' if dry_run else 'LIVE SMTP'}"
    )

    if args.mode == "once":
        process_reminders(dry_run=dry_run, logger=logger)
    else:
        run_scheduler(dry_run=dry_run, interval_seconds=args.interval, logger=logger)


if __name__ == "__main__":
    main()