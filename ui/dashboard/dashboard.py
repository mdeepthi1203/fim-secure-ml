import json
from pathlib import Path


LOG_FILE = Path(__file__).resolve().parent.parent / "storage" / "audit_logs.jsonl"


def show_dashboard():
    if not LOG_FILE.exists():
        print("No audit logs found.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)

            severity = entry.get("alert_severity", "INFO")
            file_path = entry.get("file_path", "unknown")
            integrity = entry.get("integrity_status", "unknown")

            # Simple ML label mapping (for demo)
            if severity == "CRITICAL":
                ml_label = "Malicious"
            elif severity == "WARNING":
                ml_label = "Suspicious"
            else:
                ml_label = "Benign"

            print(
                f"[{severity}] {file_path} | Integrity={integrity} | ML={ml_label}"
            )


if __name__ == "__main__":
    show_dashboard()
