from .models import Courier
# insert here methods associated to solving/storing the results of the call to the api

def process_orders():
    from core.models import Order, Sender, Receiver

    api = Courier.objects.first()
    orders = api.get_orders()['orders']
    if orders:
        for order in orders:
            sender_data = order['sender_info']
            receiver_data = order['receiver_info']

            sender, created = Sender.objects.update_or_create(
                name = sender_data['name'],
                street_and_number = sender_data['street_and_number'],
                zipcode = sender_data['zipcode'],
                city = sender_data['city'],
                country = sender_data['country'],
            )

            receiver, created = Receiver.objects.update_or_create(
                name = receiver_data['name'],
                street_and_number = receiver_data['street_and_number'],
                zipcode = receiver_data['zipcode'],
                city = receiver_data['city'],
                country = receiver_data['country'],
            )

            order, created = Order.objects.update_or_create(
                external_id = order['id'],
                send_date = order['send_date'], # might need processing
                size_x = order['x_in_mm'],
                size_y = order['y_in_mm'],
                size_z = order['z_in_mm'],
                is_breakable = order['is_breakable'],
                is_perishable = order['is_perishable'],
                sender = sender,
                receiver = receiver
            )
    else:
        pass # log error if time

def make_offer(price, delivery_time, order_id):
    pass

def get_delivery(delivery_id):
    pass

def update_delivery(delivery_id, status):
    pass

def upload_label(delivery_id, label):
    pass