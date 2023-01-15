import requests

headers = {
    "x-api-key": "6PZ72rtcNiDxrjgdV5Qd",
    "accept": "application/json"
}

r = requests.get(url="https://pasd-webshop-api.onrender.com/api/order/", headers=headers)


r.json()