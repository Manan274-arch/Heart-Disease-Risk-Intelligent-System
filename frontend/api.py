import requests

API_URL = "https://your-render-url/predict"

def get_prediction(data):
    try:
        response=requests.post(API_URL, json=data)
        return response.json()
    except Exception:
        return {"error":"Backend not running"}