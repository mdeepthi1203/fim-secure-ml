import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("ml/fim_ml_dataset_feature_engineered.csv")

print(df.head())
print("\nLabel distribution:")
print(df["label"].value_counts())

# -----------------------------
# Feature selection (EXACT)
# -----------------------------
FEATURE_COLUMNS = [
    "file_extension",
    "process_type",
    "size_before_kb",
    "size_after_kb",
    "time_gap_seconds",
    "files_modified_in_window",
    "filename_entropy",
    "size_change_ratio",
    "is_executable",
    "high_entropy_flag",
    "mass_change_flag"
]

X = df[FEATURE_COLUMNS]
y = df["label"]

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# -----------------------------
# Preprocessing
# -----------------------------
categorical_cols = ["file_extension", "process_type"]
numerical_cols = [c for c in FEATURE_COLUMNS if c not in categorical_cols]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

# -----------------------------
# Model
# -----------------------------
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight="balanced",
    random_state=42
)

pipeline = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("model", rf)
])

# -----------------------------
# Train
# -----------------------------
pipeline.fit(X_train, y_train)
print("\nModel training completed")

# -----------------------------
# Feature importance
# -----------------------------
feature_names = pipeline.named_steps["preprocess"].get_feature_names_out()
importances = pipeline.named_steps["model"].feature_importances_

fi = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print("\nTop 10 important features:")
print(fi.head(10))
# -----------------------------
# Evaluation on test data
# -----------------------------
y_pred = pipeline.predict(X_test)
# -----------------------------
# Evaluation Metrics
# -----------------------------
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label="malicious")
recall = recall_score(y_test, y_pred, pos_label="malicious")
f1 = f1_score(y_test, y_pred, pos_label="malicious")

cm = confusion_matrix(y_test, y_pred)
TN, FP, FN, TP = cm.ravel()
false_positive_rate = FP / (FP + TN)

print("\nEvaluation Metrics:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")
print(f"False Positive Rate: {false_positive_rate:.4f}")

print("\nConfusion Matrix:")
print(cm)
# -----------------------------
# Feature importance
# -----------------------------
feature_names = pipeline.named_steps["preprocess"].get_feature_names_out()
importances = pipeline.named_steps["model"].feature_importances_
...

# -----------------------------
# Save model
# -----------------------------
joblib.dump(pipeline, "ml/fim_rf_model.pkl")
print("\nModel saved as ml/fim_rf_model.pkl")
