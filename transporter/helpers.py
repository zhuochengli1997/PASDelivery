from .models import Courier
# insert here methods associated to solving/storing the results of the call to the api

def process_orders():
    from core.models import Order, Sender, Receiver, Parcel

    api = Courier.objects.first()
    orders = api.get_orders()['orders']
    if orders:
        for order in orders:
            print(order['last_delivery'])
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

            order_obj = Order.objects.filter(external_id = order['id']) or None

            if order_obj:
                order_obj = order_obj.first()
                
            else:
                order_obj  = Order.objects.create(
                    external_id = order['id'],
                    send_date = order['send_date'], 
                    size_x = order['x_in_mm'],
                    size_y = order['y_in_mm'],
                    size_z = order['z_in_mm'],
                    is_breakable = order['is_breakable'],
                    is_perishable = order['is_perishable'],
                    sender = sender,
                    receiver = receiver,
                )

            if order['last_delivery'] != None:
                order_obj.last_delivery = order['last_delivery']
                order_obj.save()

                if not order_obj.parcel:
                    parcel = Parcel.objects.create(
                        external_id = order['last_delivery']['id'],
                        expected_deliver_datetime = order['last_delivery']['expected_deliver_datetime'],
                        actual_deliver_datetime = order['last_delivery']['actual_deliver_datetime'],
                        cost_in_cents = order['last_delivery']['cost_in_cents'],
                        status = order['last_delivery']['status'],
                    )
                    order_obj.parcel = parcel
                    order_obj.save()
            
    else:
        pass # log error if time

def make_offer(price, delivery_time, order_id):
    from core.models import Parcel, Order
    print('running')
    api = Courier.objects.first()
    successful, offer_reply = api.send_offer(price,delivery_time,order_id)
    print(offer_reply)
    if successful:
        if offer_reply['status']!="REJ":
            order = Order.objects.get(external_id=order_id),
            order.last_delivery = offer_reply
            order.save()
            parcel = Parcel.objects.create(
                external_id = offer_reply['id'],
                order = Order.objects.get(external_id=order_id),
                expected_deliver_datetime = offer_reply['expected_deliver_datetime'],
                actual_deliver_datetime = offer_reply['actual_deliver_datetime'],
                cost_in_cents = offer_reply['cost_in_cents'],
                status = "EXP",
            )
        return 0
    elif offer_reply:
        return 1

def get_delivery(delivery_id):
    from core.models import Parcel, Order
    api = Courier.objects.first()
    delivery = api.get_delivery_by_id(delivery_id)
    if delivery:
        parcel=Parcel.objects.create(
            external_id = delivery['id'],
            order = Order.objects.get(external_id = delivery['order_id']),
            expected_deliver_datetime = delivery['expected_deliver_datetime'],
            actual_deliver_datetime = delivery['actual_deliver_datetime'],
            cost_in_cents = delivery['cost_in_cents'],
            status = delivery['status'],
        ) 
    else:
        pass

def update_delivery(delivery_id, status):
    from core.models import Parcel, Order
    api = Courier.objects.first()
    delivery = api.get_delivery_by_id(delivery_id)
    if delivery:
        api.update_delivery_by_id(delivery_id,status)
    else:
        pass

def upload_label(delivery_id, label):
    api = Courier.objects.first()
    delivery = api.get_delivery_by_id(delivery_id)
    if delivery:
        api.send_label(delivery_id,label)
    pass