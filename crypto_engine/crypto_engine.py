# ==========================================================
# CRYPTO MODULE – FROZEN
# Do not modify without team discussion
# Phases 1–3 complete:
# - HMAC-SHA3-256
# - Persistent baseline storage
# - Secure key management (env-based)
# ==========================================================
import os
import hmac
from Crypto.Hash import SHA3_256
import json
from pathlib import Path
BASELINE_FILE = Path(__file__).parent / "baselines.json"


def generate_hmac(file_path: str, secret_key: bytes) -> str:
    """
    Generate HMAC-SHA3-256 for a given file.
    """
    hmac_obj = hmac.new(secret_key, digestmod=SHA3_256)

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hmac_obj.update(chunk)

    return hmac_obj.hexdigest()


def verify_integrity(file_path: str, baseline_hmac: str, secret_key: bytes) -> str:
    """
    Verify file integrity by comparing current HMAC with baseline.
    """
    current_hmac = generate_hmac(file_path, secret_key)

    if hmac.compare_digest(current_hmac, baseline_hmac):
        return "MATCH"
    else:
        return "MISMATCH"

def load_baselines() -> dict:
    if BASELINE_FILE.exists():
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    return {}
def save_baselines(baselines: dict) -> None:
    with open(BASELINE_FILE, "w") as f:
        json.dump(baselines, f, indent=4)
def verify_with_baseline(file_path: str, secret_key: bytes) -> str:
    baselines = load_baselines()
    file_path = str(Path(file_path).resolve())

    if file_path not in baselines:
        baselines[file_path] = generate_hmac(file_path, secret_key)
        save_baselines(baselines)
        return "BASELINE_CREATED"

    baseline_hmac = baselines[file_path]
    return verify_integrity(file_path, baseline_hmac, secret_key)

def get_secret_key() -> bytes:
    key = os.getenv("FIM_SECRET_KEY")
    if not key:
        raise RuntimeError("FIM_SECRET_KEY not set in environment")
    return key.encode()
def crypto_check(file_path: str) -> dict:
    secret_key = get_secret_key()

    status = verify_with_baseline(file_path, secret_key)
    hmac_value = generate_hmac(file_path, secret_key)

    return {
        "file_path": str(Path(file_path).resolve()),
        "hmac": hmac_value,
        "integrity_status": status
    }
