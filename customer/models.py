from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending')

