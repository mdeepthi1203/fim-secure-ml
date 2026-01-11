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
