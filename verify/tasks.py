import os
import requests
from celery import Celery
from verification.environments import API_KEY

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379/0')

API_KEY = API_KEY
SMS_ENDPOINT = "https://api.sms.ir/v1/send/verify"


@app.task()
def send_code(mobile, random_code):
    data = {
        "mobile": mobile,
        "templateId": 100000,
        "parameters": [
            {
                "name": "Code",
                "value": random_code
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/plain",
        "x-api-key": API_KEY
    }
    response = requests.post(SMS_ENDPOINT, json=data, headers=headers)
    print(response.json())