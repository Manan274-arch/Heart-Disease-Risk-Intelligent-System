# Heart Disease Risk Stratification System

A full-stack ML project that predicts and explains cardiovascular risk using calibrated probabilities and an ensemble of models.

---

## Overview

- Predicts heart disease risk as a probability (0–1)
- Converts probability into risk categories:
  - Low (< 0.30)
  - Medium (0.30 – 0.80)
  - High (> 0.80)
- Provides SHAP-based explanations for interpretability

---

## ML Pipeline

- Dataset: heart.csv
- Models:
  - RandomForest
  - XGBoost
  - LightGBM
- Ensemble: weighted soft voting (0.30 / 0.35 / 0.35)
- SMOTE applied on training data only
- Calibration: Isotonic Regression

---

## Backend (FastAPI)

Endpoint: `/predict`

Steps:
1. Preprocess input (encoding + feature alignment)
2. Model predictions
3. Ensemble output
4. Calibration
5. Risk categorization
6. SHAP explanations

---

## Frontend (Streamlit)

Pages:
- Assessment (input form)
- Results (risk score + category)
- Insights (feature contributions using SHAP)

---

## Project Structure
backend/
frontend/
models/
data/


---

## Tech Stack

- Python
- Scikit-learn
- XGBoost
- LightGBM
- FastAPI
- Streamlit
- SHAP

---

## Note
Trained model files are not included in this repository. 
Run the training script to generate them before starting the backend.
This project is for educational purposes and not intended for medical diagnosis.