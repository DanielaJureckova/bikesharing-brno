import pandas as pd
import json

with open("test_weather.json", mode="r", encoding="utf-8") as file:
    data = json.load(file)

daily_data = pd.DataFrame(data["daily"])
hourly_data = pd.DataFrame(data["hourly"])

print(daily_data.shape)
print(hourly_data.head())