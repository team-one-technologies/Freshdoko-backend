from django.db import models
from django.contrib.auth.models import User

class Crop(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    planting_date = models.DateTimeField()
    harvest_date = models.DateTimeField()
    crop_image = models.ImageField(upload_to='crop_images/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    weather_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.crop_name
