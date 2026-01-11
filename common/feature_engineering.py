import math

def extract_features(file_event, crypto_result):
    """
    Converts raw file system event + crypto output
    into ML-ready features.
    """

    old_size = file_event.get("old_size", 0)
    new_size = file_event.get("new_size", 0)

    features = {
        # File attributes
        "file_extension": file_event["file_path"].split(".")[-1],
        "process_type": file_event["process"],

        # Size features
        "size_before_kb": old_size // 1024,
        "size_after_kb": new_size // 1024,
        "size_change_ratio": new_size / max(old_size, 1),

        # Time & frequency (placeholders allowed)
        "time_gap_seconds": 0,
        "files_modified_in_window": 1,

        # Entropy related (placeholder for demo)
        "filename_entropy": 3.5,
        "high_entropy_flag": 0,

        # Execution & mass change
        "is_executable": int(
            file_event["file_path"].endswith((".exe", ".sh"))
        ),
        "mass_change_flag": 0
    }

    return features

if __name__ == "__main__":
    file_event = {
        "file_path": "test.exe",
        "process": "powershell",
        "old_size": 2048,
        "new_size": 4096
    }

    crypto_result = {
        "integrity_status": "MISMATCH"
    }

    features = extract_features(file_event, crypto_result)
    print(features)
