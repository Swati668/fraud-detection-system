import os
import requests

API_URL = os.getenv(
    "API_URL",
    "http://localhost:5001"
)

def predict_transaction(payload):

    response = requests.post(
        f"{API_URL}/fraud/predict",
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    return response.json()