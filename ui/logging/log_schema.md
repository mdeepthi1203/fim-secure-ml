## Security Audit Log Schema

Each event is logged as a single JSON object.

Fields:
- timestamp (ISO-8601)
- file_path
- integrity_status
- crypto_version
- ml_prediction
- ml_label
- alert_generated
- alert_severity
- alert_reason
- file_metadata
