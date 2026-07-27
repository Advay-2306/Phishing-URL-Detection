"""Retrain the phishing detector, scoped to plain domain-style URLs.

Two things differ from train_model.py / train_model_url_only.py:

1. Feature values are not read from the dataset's precomputed columns - they
   are recomputed straight from the raw `url` column using
   ml_service.utils.feature_extractor.extract_features_v2, the exact same
   function the live API calls at inference time. This guarantees zero
   train/serve skew.

2. Scope is deliberately narrowed to the *domain* part of the URL (scheme +
   optional www/subdomain + registrable domain + a recognized extension).
   Path/query content is intentionally not scored. Early iterations that did
   score full-URL/path statistics learned "does this URL have a path" as a
   proxy for phishing, because this dataset's legitimate URLs skew heavily
   toward bare homepages - which meant completely ordinary pages like
   github.com/login or accounts.google.com/ServiceLogin got flagged as
   phishing. Restricting scope to the hostname avoids that failure mode, at
   the cost of missing phishing tactics that only show up in a URL's path or
   query string (a known, accepted limitation - see README).

The dataset also has its own bias worth calling out: ~84% of legitimate
examples have a "www." subdomain vs ~21% of phishing ones, so a model trained
on it as-is learns "no www subdomain => phishing", which flags plenty of
modern sites that skip www by default (github.com, amazon.com, netflix.com...).
We counter this directly with light data augmentation: every training URL
that has a "www." prefix gets a bare-domain duplicate added with the same
label, since they're the same site. This doesn't fabricate labels - it just
stops the training set from implying that dropping "www." changes legitimacy.
"""
import pandas as pd
import joblib
from pathlib import Path
from urllib.parse import urlsplit
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, roc_auc_score, brier_score_loss

from ml_service.utils.feature_extractor import extract_features_v2


def augment_with_bare_domain_variants(urls, targets):
    """For every URL whose host starts with 'www.', add a bare-domain
    duplicate with the same label - example.com and www.example.com are the
    same site, so this corrects the dataset's www-skew without inventing
    labels."""
    aug_urls, aug_targets = [], []
    for u, t in zip(urls, targets):
        aug_urls.append(u)
        aug_targets.append(t)
        candidate = u if "://" in u else f"http://{u}"
        hostname = urlsplit(candidate).hostname or ""
        if hostname.startswith("www."):
            aug_urls.append(u.replace("://www.", "://", 1))
            aug_targets.append(t)
    return aug_urls, aug_targets


# Load dataset (only the url + status columns are used; all model features are
# recomputed from the raw URL, not taken from the dataset's own precomputed columns)
df = pd.read_csv("data/dataset_phishing.csv")
df["target"] = df["status"].map({"legitimate": 0, "phishing": 1})

urls_train, urls_test, y_train_raw, y_test_raw = train_test_split(
    df["url"], df["target"], test_size=0.2, random_state=42, stratify=df["target"]
)

aug_urls_train, aug_y_train = augment_with_bare_domain_variants(
    urls_train.tolist(), y_train_raw.tolist()
)
print(f"Training rows: {len(urls_train)} -> {len(aug_urls_train)} after www augmentation")

print("Extracting domain-scoped lexical features...")
X_train = pd.DataFrame([extract_features_v2(u) for u in aug_urls_train])
y_train = pd.Series(aug_y_train)
X_test = pd.DataFrame([extract_features_v2(u) for u in urls_test])[X_train.columns]
y_test = y_test_raw.reset_index(drop=True)
print(f"Feature matrix: {X_train.shape}")

base_model = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
model = CalibratedClassifierCV(base_model, method="isotonic", cv=5)
model.fit(X_train, y_train)

proba_test = model.predict_proba(X_test)[:, 1]
pred_test = (proba_test >= 0.5).astype(int)

print("\nClassification Report:")
print(classification_report(y_test, pred_test, target_names=["legitimate", "phishing"]))
print(f"ROC-AUC: {roc_auc_score(y_test, proba_test):.4f}")
print(f"Brier score: {brier_score_loss(y_test, proba_test):.4f}")

# Save model
model_path = Path("models/phishing_model_rf_3.joblib")
model_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, model_path)
print(f"\nModel saved successfully at: {model_path}")
