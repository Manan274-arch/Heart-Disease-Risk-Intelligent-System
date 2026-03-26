from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import pickle
import os
import shap

app=FastAPI()

# -----------------------------
# Load artifacts ONCE
# -----------------------------

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

rf = joblib.load(os.path.join(MODEL_DIR, "rf.pkl"))
xgb = joblib.load(os.path.join(MODEL_DIR, "xgb.pkl"))
lgb = joblib.load(os.path.join(MODEL_DIR, "lgb.pkl"))
calibrator = joblib.load(os.path.join(MODEL_DIR, "calibrator.pkl"))
features = joblib.load(os.path.join(MODEL_DIR, "features.pkl"))
thresholds = joblib.load(os.path.join(MODEL_DIR, "risk_thresholds.pkl"))

# SHAP explainer (XGB)
explainer=shap.TreeExplainer(xgb)

# weights
w_rf=0.30
w_xgb=0.35
w_lgb=0.35


# -----------------------------
# Input schema
# -----------------------------

class Patient(BaseModel):
    Age:int
    Sex:str
    ChestPainType:str
    RestingBP:int
    Cholesterol:int
    FastingBS:int
    RestingECG:str
    MaxHR:int
    ExerciseAngina:str
    Oldpeak:float
    ST_Slope:str


# -----------------------------
# Preprocessing
# -----------------------------

def preprocess(data):
    df=pd.DataFrame([data])
    df=pd.get_dummies(df)

    # align with training features
    df=df.reindex(columns=feature_columns, fill_value=0)

    return df


# -----------------------------
# Risk bucket
# -----------------------------

def get_risk(score):
    low_max,medium_max=thresholds

    if score<low_max:
        return "Low"
    elif score<medium_max:
        return "Medium"
    else:
        return "High"


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def home():
    return {"message":"Heart Risk API running"}


@app.post("/predict")
def predict(patient:Patient):

    X=preprocess(patient.dict())

    # -----------------------------
    # Model probabilities
    # -----------------------------
    rf_p=rf.predict_proba(X)[:,1][0]
    xgb_p=xgb.predict_proba(X)[:,1][0]
    lgb_p=lgb.predict_proba(X)[:,1][0]

    # -----------------------------
    # Ensemble
    # -----------------------------
    ensemble=(
        w_rf*rf_p+
        w_xgb*xgb_p+
        w_lgb*lgb_p
    )

    # -----------------------------
    # Calibration
    # -----------------------------
    calibrated=calibrator.predict([ensemble])[0]
    calibrated=float(np.clip(calibrated,0,1))

    # -----------------------------
    # Risk bucket
    # -----------------------------
    category=get_risk(calibrated)

    # -----------------------------
    # SHAP EXPLANATION (SAFE VERSION)
    # -----------------------------
    top_factors=[]

    try:
        print("Before SHAP")

        shap_values=explainer(X)   # NEW API (important)
        shap_vals=shap_values.values[0]

        feature_impact=dict(zip(feature_columns, shap_vals))

        top_features=sorted(
            feature_impact.items(),
            key=lambda x:abs(x[1]),
            reverse=True
        )[:5]

        top_factors=[
            {
                "feature":f,
                "impact":round(float(v),4),
                "effect":"increase" if v>0 else "decrease"
            }
            for f,v in top_features
        ]

        print("After SHAP")

    except Exception as e:
        print("SHAP ERROR:", e)
        top_factors=[]

    # -----------------------------
    # Response
    # -----------------------------
    return {
        "risk_score":round(calibrated,4),
        "risk_category":category,
        "top_factors":top_factors
    }