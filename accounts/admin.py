# accounts/admin.py

from django.contrib import admin
from .models import User, Product , Crop
from .admin_site import admin_site  # Import the custom admin site

@admin.register(User, site=admin_site)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "short_desc", "weight", "price")


@admin.register(Crop,site=admin_site)
class CropAdmin(admin.ModelAdmin):
    list_display=("crop_name","short_desc" , "batch_number" ,"batch_quantity")

