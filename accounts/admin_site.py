# accounts/admin_site.py

from django.contrib.admin import AdminSite
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class CustomAdminSite(AdminSite):
    site_header = "FreshDoko Admin"
    site_title = "FreshDoko Admin Portal"
    index_title = "Welcome to the FreshDoko Admin Portal"

    def has_permission(self, request):
        # Only allow users with 'admin' user_type to access the admin interface
        if request.user.is_authenticated:
            # Ensure user_type exists and is 'admin'
            if hasattr(request.user, 'user_type') and request.user.user_type == 'admin':
                return True
        # Optionally, redirect or show a custom message
        return False

# Assign the custom admin site
admin_site = CustomAdminSite(name='custom_admin')
