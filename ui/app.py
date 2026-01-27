import json

from alerts.alert_engine import evaluate_event
from logging.audit_logger import log_event


def run_pipeline(payload_path: str):
    # 1. Load mock payload
    with open(payload_path, "r") as f:
        event = json.load(f)

    # 2. Run alert engine
    alert_decision = evaluate_event(event)

    # 3. Build final log entry
    log_entry = {
        **event,
        **alert_decision
    }

    # 4. Write to audit log
    log_event(log_entry)

    return log_entry


if __name__ == "__main__":
    # Change file here to test different cases
    result = run_pipeline("test_payloads/malicious.json")

    print("Pipeline output:")
    print(result)
