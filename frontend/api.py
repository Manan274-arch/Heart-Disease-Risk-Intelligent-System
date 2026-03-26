import requests

API_URL = "https://heart-disease-risk-intelligent-system.onrender.com/predict"

def get_prediction(data):
    try:
        response=requests.post(API_URL, json=data)
        return response.json()
    except Exception:
        return {"error":"Backend not running"}