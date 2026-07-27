import joblib
from pathlib import Path
from ..utils.feature_extractor import extract_features, extract_features_v2

# Calibrated RandomForest scoped to domain-style URLs, trained on lexical
# features recomputed straight from the URL string (see
# train_model_calibrated.py) - no train/serve skew, better-calibrated
# confidence than the old rf_2 model, and no longer flags ordinary
# subdomain/path URLs (github.com/login, accounts.google.com/...) as phishing.
_PRIMARY_MODEL_PATH = Path("models/phishing_model_rf_3.joblib")
# Original URL-only RandomForest - kept as a fallback in case the primary model
# is missing (e.g. not yet retrained/committed in this environment).
_FALLBACK_MODEL_PATH = Path("models/phishing_model_rf_2.joblib")

model = None
feature_fn = None

def load_model():
    global model, feature_fn
    if _PRIMARY_MODEL_PATH.exists():
        model = joblib.load(_PRIMARY_MODEL_PATH)
        feature_fn = extract_features_v2
        print(f"Model loaded successfully: {_PRIMARY_MODEL_PATH}")
    elif _FALLBACK_MODEL_PATH.exists():
        model = joblib.load(_FALLBACK_MODEL_PATH)
        feature_fn = extract_features
        print(f"Primary model not found - falling back to {_FALLBACK_MODEL_PATH}")
    else:
        print("No model found - using dummy fallback")


def predict_url(url: str):
    if model is None:
        load_model()

    if model is None:
        return {"is_phishing": False, "confidence": 0.5, "features": {}}

    features_dict = feature_fn(url)
    # Convert features to the order expected by model
    feature_vector = [features_dict.get(col, 0) for col in model.feature_names_in_]

    prediction = model.predict([feature_vector])[0]
    probability = model.predict_proba([feature_vector])[0].max()

    return {
        "is_phishing": bool(prediction),
        "confidence": float(probability),
        "features": features_dict
    }