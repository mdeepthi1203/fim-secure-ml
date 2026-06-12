# ==================================================
# ML MODULE – FROZEN
# Feature schema and prediction interface finalized
# ==================================================
import os
import joblib
import pandas as pd

# Load trained model
model = joblib.load("ml/fim_rf_model.pkl")

def predict_label(file_metadata: dict):
    features = pd.DataFrame([{
        "file_extension": file_metadata["file_extension"],
        "process_type": file_metadata["process_type"],
        "size_before_kb": file_metadata["size_before_kb"],
        "size_after_kb": file_metadata["size_after_kb"],
        "time_gap_seconds": file_metadata["time_gap_seconds"],
        "files_modified_in_window": file_metadata["files_modified_in_window"],
        "filename_entropy": file_metadata["filename_entropy"],
        "size_change_ratio": file_metadata["size_change_ratio"],
        "is_executable": file_metadata["is_executable"],
        "high_entropy_flag": file_metadata["high_entropy_flag"],
        "mass_change_flag": file_metadata["mass_change_flag"]
    }])

    label = model.predict(features)[0]
    return label


if __name__ == "__main__":
    sample = {
        "file_extension": ".exe",
        "process_type": "user_edit",
        "size_before_kb": 1200,
        "size_after_kb": 1700,
        "time_gap_seconds": 10,
        "files_modified_in_window": 5,
        "filename_entropy": 4.3,
        "size_change_ratio": 1.42,
        "is_executable": 1,
        "high_entropy_flag": 1,
        "mass_change_flag": 1
    }

    result = predict_label(sample)
    print("Prediction:", result)
def predict_risk(features: dict):
    """
    Integration wrapper for file_monitor.py.
    Converts system features into ML label.
    ML model itself remains frozen.
    """

    # Map system features → ML-required schema
    file_metadata = {
        "file_extension": os.path.splitext(features["file_path"])[1],
        "process_type": features.get("event_type", "unknown").lower(),
        "size_before_kb": features.get("size_before_kb", 0),
        "size_after_kb": features.get("size_after_kb", 0),
        "time_gap_seconds": features.get("time_gap_seconds", 0),
        "files_modified_in_window": features.get("files_modified_in_window", 1),
        "filename_entropy": features.get("filename_entropy", 0),
        "size_change_ratio": features.get("size_change_ratio", 1),
        "is_executable": int(features.get("is_executable", False)),
        "high_entropy_flag": int(features.get("high_entropy_flag", False)),
        "mass_change_flag": int(features.get("mass_change_flag", False))
    }

    return predict_label(file_metadata)
