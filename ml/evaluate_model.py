from sklearn.metrics import confusion_matrix, classification_report
from train_ml_model import pipeline, X_test, y_test

y_pred = pipeline.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
