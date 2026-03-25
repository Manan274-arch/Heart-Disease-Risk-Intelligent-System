import requests

API_URL="http://127.0.0.1:8000/predict"

def get_prediction(data):
    try:
        response=requests.post(API_URL, json=data)
        return response.json()
    except Exception:
        return {"error":"Backend not running"}