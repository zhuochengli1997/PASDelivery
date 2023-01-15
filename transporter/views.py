import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Order
from django.http import HttpResponseRedirect

@login_required()
def home(request):
    return render(request,'courier.html')

@login_required()
def orders_view(request):
    from .helpers import process_orders
    from core.forms import OfferForm

    process_orders()

    return render(request, 'orders.html', context={'orders':Order.objects.all(), 'form': OfferForm()})


@login_required()
def place_offer(request, id):
    from .helpers import make_offer
    from core.forms import OfferForm
    order = Order.objects.get(external_id=id)

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            make_offer(data['price'], data['date'], data['external_id'])
            return HttpResponseRedirect('/thanks/') # TODO: make other redirect

    return render(request, 'order_offer.html', context={'order':order, 'form':OfferForm(initial={'external_id':id})})

@login_required()
def shipment_planning(request):
    return render(request, '', context={})

# TODO:
# - finish endpoints interaction.
# - add tasks I guess with celery, to form a route once you start a car
#  => make car model to which you assign orders
#  => store a route in association to a car
# => link user to route base





