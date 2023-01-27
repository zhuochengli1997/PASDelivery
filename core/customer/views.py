import logging
import stripe
import requests

from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.customer import forms
from django.conf import settings
from core.models import Job, Receiver, Customer

from core.customer import forms

stripe.api_key = settings.STRIPE_API_SECRET_KEY

@login_required()
def home(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/sign-in/?next=/customer")
def profile_page(request):

    user_form = forms.BasicUserForm(instance=request.user)


    # c = Customer.objects.create(user=request.user)

    if request.method == "POST":
        user_form = forms.BasicUserForm(request.POST,instance = request.user)
        if user_form.is_valid():
            user_form.save()
            for receiver in Receiver.objects.all():
                if receiver.name == request.user.first_name + " " + request.user.last_name:
                    receiver.user = request.user
                    receiver.save()
                    print("added receiver")

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

    has_current_job = Job.objects.filter(
        customer = current_customer,
        status__in = [
            Job.PROCESSING_STATUS,
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    ).exists()

    if has_current_job:
        messages.warning(request,"You currently have a job in process")
       # return redirect(reverse('customer:current_jobs'))

    creating_job = Job.objects.filter(customer=current_customer,status=Job.CREATING_STATUS).last()
    step1_form = forms.JobCreateStep1Form(instance=creating_job)
    step2_form = forms.JobCreateStep2Form(instance=creating_job)
    step3_form = forms.JobCreateStep3Form(instance=creating_job)

    api_key = settings.GOOGLE_MAP_API_KEY

    if request.method == "POST":
        if request.POST.get('step')=='1':

            step1_form = forms.JobCreateStep1Form(request.POST,request.FILES,instance=creating_job)
            if step1_form.is_valid():
                creating_job = step1_form.save(commit=False)
                creating_job.customer = current_customer
                creating_job.save()
                return redirect(reverse('customer:create_job'))

        elif request.POST.get('step')=='2':
            step2_form = forms.JobCreateStep2Form(request.POST,instance=creating_job)
            if step2_form.is_valid():
                creating_job = step2_form.save()
                api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(creating_job.pickup_address, api_key))
                api_response_dict = api_response.json()
                creating_job.pickup_lat = api_response_dict['results'][0]['geometry']['location']['lat']
                creating_job.pickup_lng = api_response_dict['results'][0]['geometry']['location']['lng']
                creating_job.save()
                return redirect(reverse('customer:create_job'))
        
        elif request.POST.get('step')=='3':
            
            step3_form = forms.JobCreateStep3Form(request.POST,instance=creating_job)
            if step3_form.is_valid():
                creating_job = step3_form.save()
                api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(creating_job.delivery_address, api_key))
                api_response_dict = api_response.json()
                creating_job.delivery_lat = api_response_dict['results'][0]['geometry']['location']['lat']
                creating_job.delivery_lng = api_response_dict['results'][0]['geometry']['location']['lng']
                creating_job.save()
                try:
                    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations={}&origins={}&units=imperial&key={}".format(
                        creating_job.pickup_address,
                        creating_job.delivery_address,
                        settings.GOOGLE_MAP_API_KEY,
                    ))

                    print(r.json()["rows"])

                    distance = r.json()['rows'][0]['elements'][0]['distance']['value']
                    duration = r.json()['rows'][0]['elements'][0]['duration']['value']

                    creating_job.distance = round(distance/1000,2)
                    creating_job.duration = int(duration/60)
                    creating_job.price = creating_job.distance*25 # $1 per second
                    creating_job.status = Job.PROCESSING_STATUS
                    creating_job.save()


                    
                except Exception as e:
                    print(e)
                    messages.error(request,"We do not support shipping to this location")
                
                return redirect(reverse('customer:create_job'))
   
    if not creating_job:
        current_step = 1
    elif creating_job.delivery_address:
        current_step = 4
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
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY

    })

@login_required(login_url="/sign-in/?next=/customer")
def current_jobs_page(request):
    jobs = Job.objects.filter(
        status__in=[
            Job.PROCESSING_STATUS,
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    )

    return render(request,'customer/jobs.html',{
        "jobs": jobs
    })

@login_required(login_url="/sign-in/?next=/customer")
def archived_jobs_page(request):
    jobs = Job.objects.filter(
        customer=request.user.customer,
        status__in=[
            Job.COMPLETED_STATUS,
            Job.CANCELED_STATUS
        ]
    )

    return render(request,'customer/jobs.html',{
        "jobs": jobs
    })

@login_required(login_url="/sign-in/?next=/customer")
def job_page(request,job_id):
    job = Job.objects.get(id=job_id)
    return render(request,'customer/job.html',{
        "job": job,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY
    })