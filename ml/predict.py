import joblib
import pandas as pd

# Load trained model
model = joblib.load("ml/fim_rf_model.pkl")

# 🔑 Label mapping
LABEL_MAP = {
    "benign": 0,
    "malicious": 1
}

def predict_risk(file_metadata: dict):
    """
    file_metadata example:
    {
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
    """

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

    # 🔮 Predict
    label_str = model.predict(features)[0]

    # 🔁 Map to numeric output
    return LABEL_MAP[label_str]


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

    result = predict_risk(sample)
    print("Prediction (0=Benign, 1=Malicious):", result)

