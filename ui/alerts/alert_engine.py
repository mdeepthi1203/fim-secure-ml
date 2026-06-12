def evaluate_event(event: dict) -> dict:
    """
    Decide whether an alert should be generated for a given event.
    """

    integrity_status = event.get("integrity_status", "").lower()
    severity = event.get("severity", "").upper()

    # Default response
    alert = {  
        "alert_generated": False,
        "alert_severity": "INFO",
        "alert_reason": "No suspicious activity detected"
    }

    # Logic rules
    if integrity_status == "tampered":
        alert["alert_generated"] = True
        alert["alert_severity"] = "CRITICAL"
        alert["alert_reason"] = "File integrity compromised"

    elif integrity_status == "modified":
        alert["alert_generated"] = True
        alert["alert_severity"] = "WARNING"
        alert["alert_reason"] = "File modification detected"

    return alert
