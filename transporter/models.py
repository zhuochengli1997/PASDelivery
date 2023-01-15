import requests
from django.db import models

class Courier(models.Model):
    apikey = models.TextField(default="")
    # api key: 6PZ72rtcNiDxrjgdV5Qd

    @property
    def base_url(self):
        return "https://pasd-webshop-api.onrender.com"

    @property
    def headers(self):
        return {
            "x-api-key": self.apikey,
            "accept": "application/json"
        }

    def get_orders(self):
        print(self.headers)
        r = requests.get(url=f'{self.base_url}/api/order/', headers=self.headers)
        if r.ok:
            return r.json()
        # log error
        return None

    def send_offer(self, price, delivery_time, order_id): # to test
        body = {
            "price_in_cents": price,
            "expected_delivery_datetime": delivery_time, # utz format
            "order_id": order_id
        }

        r = requests.post(url=f'{self.base_url}/api/delivery', headers=self.headers, json=body)

        if r.ok:
            return r.json()
        # status code 400 seems to mean that is already being delivered, so the offer was not placed
        return None

    def get_delivery_by_id(self, delivery_id):
        r = requests.get(url=f'{self.base_url}/api/delivery/{delivery_id}', headers=self.headers)

        if r.ok:
            return r.json()
        return None

    def update_delivery_by_id(self, delivery_id, status):
        body = {
            'status': status
        }
        r = requests.patch(url=f'{self.base_url}/api/delivery/{delivery_id}', headers=self.headers, json=body)

        if r.ok:
            return r.json()
        return None

    def send_label(self, delivery_id, label): # test for path too
        body = {
            'labelFile': label # check needed form
        }

        r = requests.post(url=f'{self.base_url}/api/label?delivery_id={delivery_id}', json=body)

        if r.ok:
            return r.json()
        return None

        