import logging
from pathlib import Path
from src.config import LOGS_DIR


def setup_logger(log_filename: str = "automation.log") -> logging.Logger:
    """Configure dual logging to both console and a rotating/persistent log file."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path: Path = LOGS_DIR / log_filename

    logger = logging.getLogger("EmailAutomation")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger