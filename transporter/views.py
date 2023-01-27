import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Order, Parcel, Schedule
from django.http import HttpResponseRedirect
from django.db.models import Q

@login_required()
def home(request):
    return render(request,'courier.html')

@login_required()
def demo(request):
    parcels = Parcel.objects.all()
    return render(request, "demo.html", context={"parcels":parcels})

@login_required()
def my_parcels_view(request, id):
    parcels = Parcel.objects.filter(order__receiver__user__id=id)

    return render(request, "my_parcels.html", context={"parcels":parcels})

@login_required()
def parcel_manager(request, id):
    parcel = Parcel.objects.get(id=id)
    timetables = Schedule.objects.get(user__id=request.user.id)
    return render(request, "parcel.html", context={"parcel":parcel, "timetables":timetables})


@login_required()
def orders_view(request):
    from .helpers import process_orders
    from core.forms import OfferForm

    process_orders()

    ids = []
    for order in Order.objects.all():
        if not order.last_delivery:
            ids.append(order.id)

    return render(request, 'orders.html', context={'orders':Order.objects.filter(id__in=ids), 'form': OfferForm()})


@login_required()
def place_offer(request, id):
    from .helpers import make_offer
    from core.forms import OfferForm
    order = Order.objects.get(external_id=id)

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            case = make_offer(data['price'], data['date'], data['external_id'])
            return redirect(f'/transporter/place_offer_result/{id}/{case}')
    if order.parcel:
        parcel = order.parcel
    else:
        parcel = None
    return render(request, 'order_offer.html', context={'order':order, 'form':OfferForm(initial={'external_id':id}), 'parcel':parcel})

@login_required()
def place_offer_result(request, id, case):
    from core.forms import OfferForm
    order = Order.objects.get(external_id=id)

    if order.parcel:
        parcel = order.parcel
    else:
        parcel = None
    context = {'order': Order.objects.get(external_id=id),  'form':OfferForm(initial={'external_id':id}), 'parcel':parcel}
    if case:
        context["detail"] = "This order is already being shipped."

    return render(request, 'order_offer_result.html', context=context)

@login_required()
def confirmed_orders(request):
    ids = []
    for order in Order.objects.all():
        if order.last_delivery:
            ids.append(order.id)

    return render(request, 'confirmed_orders.html', context={'parcels':Parcel.objects.all().prefetch_related('order')})

@login_required()
def shipment_planning(request):
    return render(request, '', context={})

# TODO:
# - finish endpoints interaction.
# - add tasks I guess with celery, to form a route once you start a car
#  => make car model to which you assign orders
#  => store a route in association to a car
# => link user to route base





