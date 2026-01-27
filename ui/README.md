## Payload Contract (Input to this Module)

This module consumes the final payload produced by:
- Crypto module (HMAC-SHA3-256)
- ML behavior analysis module

Payload format (DO NOT MODIFY):

{
  "crypto_output": {
    "file_path": "string",
    "hmac": "string",
    "integrity_status": "MATCH | MISMATCH"
  },
  "file_metadata": {
    "file_size_change": int,
    "modification_frequency": int,
    "time_since_last_change": int,
    "file_type": int
  },
  "ml_prediction": 0 | 1 | 2
}


Updated complete UI structure
