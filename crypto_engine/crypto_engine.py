import os
import hmac
from Crypto.Hash import SHA3_256


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


