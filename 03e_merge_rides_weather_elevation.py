import pandas as pd
import numpy as np


df_rides = pd.read_csv(
    './Data/merged/next_rekola_all.csv', header=0, delimiter=',')
df_weather = pd.read_csv(
    './Data/weather/weather-22-to-05-11-23.csv', header=0, delimiter=',')
# df_elevation = pd.read_csv(
#     './Data/elevation/23-10-26_data_with_location_elevation.csv', header=0, delimiter=',')


# df_elevation.drop(columns=["start_time", "end_time",
#                   "duration", "user_id", "company"], inplace=True)
# df_elevation.drop_duplicates(inplace=True)


df_rides['start_time'] = pd.to_datetime(df_rides['start_time'])
df_rides['end_time'] = pd.to_datetime(df_rides['end_time'])


df_rides['duration_min'] = (df_rides['end_time'] - df_rides['start_time']).dt.total_seconds() // 60
df_rides.drop(columns="duration", inplace=True)

# creation of join keys
df_rides['time-key'] = pd.to_datetime(df_rides['start_time']).dt.round("H")

df_weather['time-key'] = pd.to_datetime(df_weather['time'],
                                        format='mixed').dt.floor("H")

print(f"pocet pred napojenim pocasi dropovanim podle delky: {len(df_rides.index)} ")
df_rides_weather = pd.merge(df_rides, df_weather, on="time-key", how="inner")

# filter out data too short or too long
print(f"pocet pred dropovanim podle delky: {len(df_rides_weather.index)} ")
df_rides_weather = df_rides_weather[(df_rides_weather['duration_min'] > 1) & (df_rides_weather['duration_min'] < 480)]
print(f"pocet po dropovanim podle delky: {len(df_rides_weather.index)} ")

# df_rides_weather_elevation = pd.merge(
#     df_rides_weather, df_elevation, on=['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude'], how="inner")

# print(f"pocet po napojenim elevace podle delky: {len(df_rides_weather_elevation.index)} ")
#drop unnecessary columns
df_rides_weather.drop(columns=["time-key","time"], inplace=True)

#add datatime

def add_datetime_components(inputDf):
    inputDf['year'] = inputDf['start_time'].dt.year
    inputDf['month'] = inputDf['start_time'].dt.month
    inputDf['day'] = inputDf['start_time'].dt.day
    inputDf['hour'] = inputDf['start_time'].dt.hour

add_datetime_components(df_rides_weather)

#drop start_latitude = 49
df_rides_weather = df_rides_weather[df_rides_weather["start_latitude"] != 49]

print(f"pocet po dropu start = 49: {len(df_rides_weather.index)} ")

#add filter gps
df_rides_weather = df_rides_weather[
    (df_rides_weather["start_latitude"] < 49.263) & 
    (df_rides_weather["end_latitude"] < 49.263) & 
    (df_rides_weather["start_latitude"] > 49.116) & 
    (df_rides_weather["end_latitude"] > 49.116) &
    (df_rides_weather["start_longitude"] < 16.720) & 
    (df_rides_weather["end_longitude"] < 16.720) & 
    (df_rides_weather["start_longitude"] > 16.485) & 
    (df_rides_weather["end_longitude"] > 16.485)
]

print(f"pocet po odstraneni odlehlych hodnot GPS: {len(df_rides_weather.index)} ")

df_rides_weather.to_csv("./Data/merged/23-11-11_13-20_data_filtered_weather_elevation.csv", index=False)
