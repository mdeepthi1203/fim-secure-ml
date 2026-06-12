import os
import math

def extract_features(file_event, crypto_result):
    path = file_event["file_path"]
    size = file_event.get("file_size", 0)
   

    return {
        "file_path": path,
        "event_type": file_event["event_type"],

        # ML-required fields (SAFE DEFAULTS)
        "file_extension": os.path.splitext(path)[1],
        "process_type": "user_edit",
        "size_before_kb": max(size - 1, 0),
        "size_after_kb": size,
        "time_gap_seconds": 1,
        "files_modified_in_window": 1,
        "filename_entropy": math.log2(len(os.path.basename(path)) + 1),
        "size_change_ratio": 1.0,
        "is_executable": int(path.lower().endswith(".exe")),
        "high_entropy_flag": 0,
        "mass_change_flag": 0,

        # Crypto info
        "integrity_status": crypto_result["integrity_status"]
    }
