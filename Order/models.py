# order/models.py
from django.db import models
from django.conf import settings
from cart.models import Cart, CartItem
from accounts.models import Product

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('khalti', 'Khalti'),
        ('payoneer', 'Payoneer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Reference the Cart
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    delivery_point = models.CharField(max_length=255)
    delivery_date = models.DateField()  # Set by admin
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def items(self):
        return self.cart.items.all()

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
