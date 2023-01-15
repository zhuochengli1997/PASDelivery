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




