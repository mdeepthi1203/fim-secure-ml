# ==================================================
# ML MODULE – FROZEN
# Feature schema and prediction interface finalized
# ==================================================


FileEvent = {
    "file_path": str,
    "event_type": str,
    "old_size": int,
    "new_size": int,
    "timestamp": float,
    "process": str,
    "user": str
}

CryptoResult = {
    "file_path": str,
    "hmac": str,
    "integrity_status": str
}

MLResult = {
    "anomaly_score": float,
    "risk_level": str
}
