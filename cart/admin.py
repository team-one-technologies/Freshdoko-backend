from django.contrib import admin
from .models import Order ,OrderItem

from accounts.admin_site import admin_site  

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # How many empty rows to display for adding new items

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone_number', 'total_price', 'payment_method', 'delivery_date', 'created_at', 'updated_at')
    list_filter = ('payment_method', 'payment_confirmation_number', 'created_at', 'updated_at')
    search_fields = ('full_name', 'email', 'phone_number', 'id')
    inlines = [OrderItemInline]  # Include OrderItems inline in the order details page
    readonly_fields = ('created_at', 'updated_at')  # Make fields read-only in the admin interface

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optionally, filter the orders based on some logic here (e.g., only show pending orders)
        return queryset


admin_site.register(Order, OrderAdmin)

