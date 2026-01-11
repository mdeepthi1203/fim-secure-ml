from common.feature_engineering import extract_features
from ml.predict import predict_label
from common.risk_decision import make_risk_decision
from common.action_layer import take_action

# Simulated file system event
file_event = {
    "file_path": "test.exe",
    "process": "powershell",
    "old_size": 2048,
    "new_size": 4096
}

# Simulated crypto output
crypto_result = {
    "file_path": file_event["file_path"],
    "integrity_status": "MISMATCH"
}

# Feature engineering
features = extract_features(file_event, crypto_result)

# ML prediction
label = predict_label(features)

# Risk decision
final_result = make_risk_decision(
    file_event,
    crypto_result,
    label
)

# Action layer
take_action(final_result)

print("\nFinal Output:")
print(final_result)
