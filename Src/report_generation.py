import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pandas as pd


def save_execution_report(
    records: List[Dict[str, str]],
    outputs_dir: Path,
    logger: logging.Logger,
) -> Path:
    """Save email execution results to a timestamped CSV and update latest_report.csv."""
    outputs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = outputs_dir / f"email_report_{timestamp}.csv"
    latest_path = outputs_dir / "latest_report.csv"

    df = pd.DataFrame(records)
    df.to_csv(report_path, index=False, encoding="utf-8")
    df.to_csv(latest_path, index=False, encoding="utf-8")

    logger.info(f"Report generated: {report_path}")
    return report_path