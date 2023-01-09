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
    current_customer = request.user.customer
    creating_job = Job()
    step1_form = forms.JobCreateStep1Form(instance=creating_job)
    step2_form = forms.JobCreateStep2Form(instance=creating_job)
    step3_form = forms.JobCreateStep3Form(instance=creating_job)

    if request.method == "POST":
        if request.POST.get('step')==1:
            step1_form = forms.JobCreateStep1Form()
            if step1_form.is_valid:
                creating_job = step1_form.save(commit=False)
                creating_job.customer = current_customer
                creating_job.save()
                return redirect(reverse('customer:create_job'))
        elif request.POST.get('step')=='2':
            step2_form = forms.JobCreateStep2Form(request.POST,instance=creating_job)
            if step2_form.is_valid():
                creating_job = step2_form.save()
                return redirect(reverse('customer:create_job'))
   
    if not creating_job:
        current_step = 1
    elif creating_job.pickup_name:
        current_step = 3
    else:
        current_step = 2


    return render(request,'customer/create_job.html',{
        "job": creating_job,
        "step": current_step,
        "step1_form": step1_form,
        "step2_form": step2_form,
        "step3_form": step3_form,

    })
