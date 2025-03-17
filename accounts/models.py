from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('farmer', 'Farmer'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Crop(models.Model):
    # Linking the crop to the farmer (user)
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="crops")

    # Crop details
    crop_gallery = models.ImageField(upload_to='crop_images/', blank=True, null=True)
    crop_name = models.CharField(max_length=255)
    short_desc = models.TextField()
    batch_number = models.CharField(max_length=100)
    batch_quantity = models.PositiveIntegerField()
    harvest_date = models.DateField()
    storage_date = models.DateField()

    def __str__(self):
        return f"{self.crop_name} - {self.batch_number}"
    


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    short_desc = models.TextField()
    weight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dimension = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=100)
    crop_batch_number = models.CharField(max_length=100)
    batch_quantity = models.PositiveIntegerField()
    storage_date = models.DateField()
    packaging_date = models.DateField()
    farmer_name = models.CharField(max_length=255)
    farmer_desc = models.TextField()
    slug = models.SlugField(unique=True, blank=True)  # Define the slug field

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.product_name)  # Use correct field name
            unique_slug = base_slug
            counter = 1

            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug  # Assign the final unique slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name      


class ProductGallery(models.Model):
    # Link the images to the product
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Product images

    def __str__(self):
        return f"Image for {self.product.product_name}"
