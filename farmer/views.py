from django.shortcuts import render
from .models import Crop 
from .weather import get_weather_data , get_geolocation

def create_crop(request):
    if request.method=="POST":
        crop_name=request.POST['crop_name']
        quantity=request.POST['quantity']
        planting_date = request.POST['planting_date']
        harvest_date = request.POST['harvest_date']
        location = request.POST['location']
        crop_image = request.FILES.get('crop_image')

       
        weather_data = get_weather_data(location)

        
        crop = Crop(
            farmer=request.user,
            crop_name=crop_name,
            quantity=quantity,
            planting_date=planting_date,
            harvest_date=harvest_date,
            crop_image=crop_image,
            location=location,
            weather_data=weather_data
        )
        crop.save()