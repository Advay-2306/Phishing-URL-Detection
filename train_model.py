import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv("data/dataset_phishing.csv")

# Prepare target
df["target"] = df["status"].map({"legitimate": 0, "phishing": 1})

# Features and target
X = df.drop(columns=["status", "target", "url"], errors="ignore")  # drop identifiers
y = df["target"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("Classification Report:")
print(classification_report(y_test, model.predict(X_test)))

# Save model
model_path = Path("models/phishing_model_rf.joblib")
model_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, model_path)
print(f"Model saved successfully at: {model_path}")