import json
from datetime import datetime
from pathlib import Path

# Path to audit log file
LOG_FILE = Path(_file_).resolve().parent.parent / "storage" / "audit_logs.jsonl"


def log_event(event: dict):
    """
    Appends a single security event to the audit log.
    One event = one JSON line.
    """

    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(event, f)
        f.write("\n")