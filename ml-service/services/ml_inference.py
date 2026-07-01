import joblib
from pathlib import Path
from ..utils.feature_extractor import extract_features

model = None

def load_model():
    global model
    model_path = Path("models/phishing_model_rf_2.joblib")
    if model_path.exists():
        model = joblib.load(model_path)
        print("Model loaded successfully")
    else:
        print("Model not found - using dummy for now")


def predict_url(url: str):
    if model is None:
        load_model()

    if model is None:
        # Fallback
        return {"is_phishing": False, "confidence": 0.5, "features": {}}

    features_dict = extract_features(url)
    # Convert features to the order expected by model
    feature_vector = [features_dict.get(col, 0) for col in model.feature_names_in_]

    prediction = model.predict([feature_vector])[0]
    probability = model.predict_proba([feature_vector])[0].max()

    return {
        "is_phishing": bool(prediction),
        "confidence": float(probability),
        "features": features_dict
    }