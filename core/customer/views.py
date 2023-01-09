import stripe

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.customer import forms
from django.conf import settings
from core.models import Job

from core.customer import forms

stripe.api_key = settings.STRIPE_API_SECRET_KEY

@login_required()
def home(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/sign-in/?next=/customer")
def profile_page(request):

    user_form = forms.BasicUserForm(instance=request.user)

    if request.method == "POST":
        user_form = forms.BasicUserForm(request.POST,instance = request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('customer:profile'))


    return render(request,'customer/profile.html',{
        "user_form":user_form
    })

@login_required(login_url="/sign-in/?next=/customer")
def payment_method_page(request):
    current_customer = request.user.customer
    #save stripe customer info
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save

    intent = stripe.SetupIntent.create(
        customer = current_customer.stripe_customer_id
    )

    return render(request,'customer/payment_method.html',{
        "client_secret": intent.client_secret,
        "STRIPE_API_PUBLIC_KEY": settings.STRIPE_API_PUBLIC_KEY,
    })

@login_required(login_url="/sign-in/?next=/customer")
def create_job_page(request):
    step1_form = forms.JobCreateStep1Form
    step2_form = forms.JobCreateStep2Form
   

    return render(request,'customer/create_job.html',{
        "step1_form": step1_form,
        "step2_form": step2_form,
    })
