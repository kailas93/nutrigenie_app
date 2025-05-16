import requests
import geocoder

WEATHER_API_KEY = "2fe3dd918f4e3ff56cace2ea240731ac"  # <-- Get it from https://openweathermap.org/api

def get_location_and_weather():
    g = geocoder.ip('me')
    if not g.ok:
        return "Unknown", {"temp": None, "condition": "Unknown"}

    lat, lon = g.latlng
    city = g.city

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = {
            "temp": data["main"]["temp"],
            "condition": data["weather"][0]["description"].capitalize()
        }
        return city, weather
    else:
        return city, {"temp": None, "condition": "Unknown"}
