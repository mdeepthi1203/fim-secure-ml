import pandas as pd

df = pd.read_csv("fim_ml_dataset_feature_engineered.csv")

print(df.head())
print(df['label'].value_counts())
from sklearn.model_selection import train_test_split

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

categorical_cols = ['file_extension', 'process_type']
numerical_cols = [c for c in X.columns if c not in categorical_cols]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ]
)
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight='balanced',
    random_state=42
)
from sklearn.pipeline import Pipeline

pipeline = Pipeline(steps=[
    ('preprocess', preprocessor),
    ('model', rf)
])

pipeline.fit(X_train, y_train)

print("Model training completed")

import pandas as pd

feature_names = pipeline.named_steps['preprocess'].get_feature_names_out()
importances = pipeline.named_steps['model'].feature_importances_

fi = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values(by='importance', ascending=False)

print(fi.head(10))
