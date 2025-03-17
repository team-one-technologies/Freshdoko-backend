# order/serializers.py
from rest_framework import serializers
from .models import Order
from cart.serializers import CartItemSerializer  # Import CartItemSerializer

class OrderSerializer(serializers.ModelSerializer):
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

    payment_method = serializers.ChoiceField(choices=PAYMENT_CHOICES)
    delivery_point = serializers.CharField(max_length=255)
    delivery_date = serializers.DateField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='pending')
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_method', 'delivery_point', 'delivery_date', 'total_price', 'status', 'items']
