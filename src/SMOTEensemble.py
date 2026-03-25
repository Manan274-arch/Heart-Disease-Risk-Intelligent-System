import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, roc_auc_score

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from sklearn.isotonic import IsotonicRegression
from imblearn.over_sampling import SMOTE

import joblib
import pickle
import os

print("Loading dataset...")

df = pd.read_csv("data/heart.csv")

X = df.drop("HeartDisease", axis=1)
y = df["HeartDisease"]


# -----------------------------
# Train/Test split
# -----------------------------

X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

### FIX: create validation split (for calibration)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full,
    test_size=0.25,
    random_state=42,
    stratify=y_train_full
)


# -----------------------------
# Encoding
# -----------------------------

X_train = pd.get_dummies(X_train)
X_val = pd.get_dummies(X_val)
X_test = pd.get_dummies(X_test)

X_train, X_val = X_train.align(X_val, join="left", axis=1, fill_value=0)
X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)


# -----------------------------
# SMOTE (only on TRAIN)
# -----------------------------

smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)


# -----------------------------
# MODELS
# -----------------------------

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    random_state=42
)

xgb = XGBClassifier(
    n_estimators=400,
    max_depth=5,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="logloss",
    random_state=42
)

lgb = LGBMClassifier(
    n_estimators=400,
    num_leaves=31,
    learning_rate=0.03,
    reg_alpha=0.5,
    reg_lambda=2.0,
    verbosity=-1,
    random_state=42
)


print("Training models...")

rf.fit(X_train, y_train)
xgb.fit(X_train, y_train)
lgb.fit(X_train, y_train)


# -----------------------------
# ENSEMBLE (VALIDATION for calibration)
# -----------------------------

rf_val = rf.predict_proba(X_val)[:, 1]
xgb_val = xgb.predict_proba(X_val)[:, 1]
lgb_val = lgb.predict_proba(X_val)[:, 1]

ensemble_val = (
    0.3 * rf_val +
    0.35 * xgb_val +
    0.35 * lgb_val
)


# -----------------------------
# CALIBRATION (FIXED)
# -----------------------------

### FIX: fit on validation, NOT test
iso = IsotonicRegression(out_of_bounds='clip')
iso.fit(ensemble_val, y_val)


# -----------------------------
# TEST PROBABILITIES
# -----------------------------

rf_prob = rf.predict_proba(X_test)[:, 1]
xgb_prob = xgb.predict_proba(X_test)[:, 1]
lgb_prob = lgb.predict_proba(X_test)[:, 1]

ensemble_prob = (
    0.3 * rf_prob +
    0.35 * xgb_prob +
    0.35 * lgb_prob
)

calibrated_prob = iso.transform(ensemble_prob)


# -----------------------------
# RISK STRATIFICATION
# -----------------------------

low_thresh = 0.3
high_thresh = 0.8

def assign_risk(p):
    if p < low_thresh:
        return "Low"
    elif p < high_thresh:
        return "Medium"
    else:
        return "High"

risk_categories = [assign_risk(p) for p in calibrated_prob]


# -----------------------------
# RESULTS DATAFRAME
# -----------------------------

results_df = pd.DataFrame({
    "probability": calibrated_prob,
    "risk_category": risk_categories,
    "actual": y_test.values
})


# -----------------------------
# PRIMARY METRICS (YOUR NEW GOAL)
# -----------------------------

total_positives = results_df["actual"].sum()
total_negatives = len(results_df) - total_positives

bucket_summary = results_df.groupby("risk_category").agg(
    total_patients=("actual", "count"),
    positives=("actual", "sum")
)

bucket_summary["negatives"] = bucket_summary["total_patients"] - bucket_summary["positives"]
bucket_summary["disease_rate"] = bucket_summary["positives"] / bucket_summary["total_patients"]
bucket_summary["positive_capture"] = bucket_summary["positives"] / total_positives
bucket_summary["negative_capture"] = bucket_summary["negatives"] / total_negatives

print("\n--- PRIMARY RESULTS ---")
print(bucket_summary)
print(bucket_summary["positive_capture"])

# -----------------------------
# SECONDARY METRIC (ONLY THIS)
# -----------------------------

roc_auc = roc_auc_score(y_test, calibrated_prob)

print("\n--- ROC-AUC ---")
print(f"ROC-AUC: {roc_auc:.3f}")


# -----------------------------
# SAVE MODELS + ARTIFACTS
# -----------------------------

joblib.dump(rf, "models/rf.pkl")
joblib.dump(xgb, "models/xgb.pkl")
joblib.dump(lgb, "models/lgb.pkl")
joblib.dump(iso, "models/calibrator.pkl")

joblib.dump((low_thresh, high_thresh), "models/risk_thresholds.pkl")
joblib.dump(X_train.columns.tolist(), "models/features.pkl")

print("\nAll models and risk system artifacts saved.")