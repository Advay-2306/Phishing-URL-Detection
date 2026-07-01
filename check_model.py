import joblib
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Load model and test data (adjust path if needed)
model = joblib.load("models/phishing_model_rf.joblib")

df = pd.read_csv("data/dataset_phishing.csv")

df["target"] = df["status"].map({"legitimate": 0, "phishing": 1})
X = df.drop(columns=["status", "target", "url"], errors="ignore")
y = df["target"]

# For quick check - use full data or load saved test set
y_pred = model.predict(X)

print("Confusion Matrix:")
print(confusion_matrix(y, y_pred))

# Optional: Plot
disp = ConfusionMatrixDisplay.from_predictions(y, y_pred, display_labels=["Legitimate", "Phishing"])
plt.title("Confusion Matrix")
plt.show()