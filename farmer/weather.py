import requests

def get_geolocation():
    try:
        response = requests.get("http://ipinfo.io/json")
        data = response.json()
        location = data["loc"].split(",")
        lat, lon = float(location[0]), float(location[1])
        return lat, lon
    except Exception as e:
        print(f"Error fetching geolocation: {e}")
        return None, None


lat, lon = get_geolocation()

def get_weather_data(lat, lon):
    api_key = 'dcc8afdf52dde4823f259788f3ef0e36'  
    base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    response = requests.get(base_url)
    
    if response.status_code == 200:
        return response.json()  
    else:
        return None

if lat and lon:
    weather_data = get_weather_data(lat, lon)
    