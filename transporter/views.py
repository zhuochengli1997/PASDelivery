import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Order

@login_required()
def home(request):
    return render(request,'courier.html')

@login_required()
def orders_view(request):
    from .helpers import process_orders

    process_orders()

    return render(request, 'orders.html', context={'orders':Order.objects.all()})

@login_required()
def place_offer(request, order_id):
    from .helpers import make_offer

    order = Order.objects.get(id=order_id)

    make_offer(100, order.send_date + datetime.timedelta(days=2), order_id)

    return render(request, 'order_offer.html', context={'order':order})

@login_required()
def shipment_planning(request):
    return render(request, '', context={})

# TODO:
# - finish endpoints interaction.
# - add tasks I guess with celery, to form a route once you start a car
#  => make car model to which you assign orders
#  => store a route in association to a car
# => link user to route base





