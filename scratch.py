import requests

headers = {
    "x-api-key": "6PZ72rtcNiDxrjgdV5Qd",
    "accept": "application/json",
    "Content-Type": "application/json",
}

r = requests.get(url="https://pasd-webshop-api.onrender.com/api/order/", headers=headers)

body = {
    "price_in_cents": 10,
    "expected_delivery_datetime": "2023-01-19 00:00:00+00:00", # utz format
    "order_id": 55
}


r = requests.get(url='https://pasd-webshop-api.onrender.com/api/order/', headers=headers)
r
r.json()


Parcel.objects.create(
    external_id = o.last_delivery['id'],
    order = o,
    expected_deliver_datetime = o.last_delivery['expected_deliver_datetime'] or None,
    actual_deliver_datetime = o.last_delivery['actual_deliver_datetime'] or None,
    cost_in_cents = o.last_delivery['cost_in_cents'],
    status = o.last_delivery['status'],
) 


Order.objects.filter(last_delivery__status="EXP")

for o in Order.objects.all():
    o
    o.last_delivery

from core.models import *

order = Order.objects.get(id=30)
x = order.last_delivery

x == None