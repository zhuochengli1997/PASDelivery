from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='customer/avatars/', blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255,blank=True)
    stripe_payment_id = models.CharField(max_length=255,blank=True)
    stripe_card_last4 = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Category(models.Model):
    slug = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Sender(models.Model):
    name = models.TextField()
    street_and_number = models.TextField()
    zipcode = models.TextField()
    city = models.TextField()
    country = models.TextField()

class Schedule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="schedule")
    time = models.TimeField()
    location = models.TextField()

class Receiver(models.Model):
    name = models.TextField()
    street_and_number = models.TextField()
    zipcode = models.TextField()
    city = models.TextField()
    country = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="receiver", null=True)

class Car(models.Model):
    battery_autonomy = models.IntegerField(default=500) # km left

class Shipment(models.Model):
    car = models.ForeignKey(Car, related_name="shipments", on_delete=models.CASCADE)
    # store some route

class Parcel(models.Model):
    external_id = models.IntegerField()
    expected_deliver_datetime = models.DateTimeField(null=True)
    actual_deliver_datetime = models.DateTimeField(null=True)
    cost_in_cents = models.IntegerField()
    status = models.TextField(default="REC")
    # add customer

    shipment = models.ForeignKey(Shipment, related_name="parcels", on_delete=models.CASCADE, null=True)

class Order(models.Model):
    external_id = models.IntegerField()
    send_date = models.DateTimeField()
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    size_z = models.IntegerField()
    is_breakable = models.BooleanField(default=False)
    is_perishable = models.BooleanField(default=False)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE, related_name="orders")
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE, related_name="orders")
    parcel = models.OneToOneField(Parcel, related_name="order", on_delete=models.CASCADE, null=True)
    last_delivery = models.JSONField(null=True, default=dict)
# in order to check whether an order was accepted, check if there exists a parcel associated to it

class Job(models.Model):
    SMALL_SIZE = "small"
    MEDIUM_SIZE = "medium"
    LARGE_SIZE = "large"

    SIZES = (
        (SMALL_SIZE, 'Small'),
        (MEDIUM_SIZE, 'Medium'),
        (LARGE_SIZE, 'Large'),
    )

    CREATING_STATUS = 'creating'
    PROCESSING_STATUS = 'precessing'
    PICKING_STATUS = 'picking'
    DELIVERING_STATUS = 'delivering'
    COMPLETED_STATUS = 'completed'
    CANCELED_STATUS = 'canceled'
    STATUS = (
        (CREATING_STATUS, 'Cureating'),
        (PROCESSING_STATUS, 'Processing'),
        (PICKING_STATUS, 'Picking'),
        (DELIVERING_STATUS, 'Delivering'),
        (COMPLETED_STATUS, 'Completed'),
        (CANCELED_STATUS, 'Canceled'),
    )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category =  models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    size = models.CharField(max_length=20,choices=SIZES,default=MEDIUM_SIZE)
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='job/photos/')
    status = models.CharField(max_length=20,choices=STATUS,default=CREATING_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    pickup_address = models.CharField(max_length=255,blank=True)
    pickup_lat = models.FloatField(default=0)
    pickup_lng = models.FloatField(default=0)
    pickup_name = models.CharField(max_length=255,blank=True)
    pickup_phone = models.CharField(max_length=50,blank=True)

    delivery_address = models.CharField(max_length=255,blank=True)
    delivery_lat = models.FloatField(default=0)
    delivery_lng = models.FloatField(default=0)
    delivery_name = models.CharField(max_length=255,blank=True)
    delivery_phone = models.CharField(max_length=50,blank=True)

    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    price = models.FloatField(default=0)

    pickup_photo = models.ImageField(upload_to='job/pickup_photos/',null=True,blank=True)
    pickedup_at = models.DateTimeField(null=True,blank=True)

    delivery_photo = models.ImageField(upload_to='job/pickup_photos/',null=True,blank=True)
    delivered_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.description

