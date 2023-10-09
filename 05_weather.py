import requests
import json

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 49.20,
    "longitude": 16.61,
    "start_date": "2023-09-03",
    "end_date": "2023-09-04",
    "hourly": "temperature_2m,rain,snowfall,is_day",
    "daily": "sunrise,sunset",
    "timezone": "auto",
}

response = requests.get(url, params=params)
data = response.json()
with open("test_pocasi.json", mode="w", encoding="utf-8") as weather_file:
    json.dump(data, weather_file, ensure_ascii = False, indent=4)
