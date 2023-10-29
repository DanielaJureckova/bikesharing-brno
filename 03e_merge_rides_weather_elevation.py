import pandas as pd
import numpy as np


df_rides = pd.read_csv(
    './Data/merged/next_rekola_both.csv', header=0, delimiter=',')
df_weather = pd.read_csv(
    './Data/weather/weather-22-to-15-10-23.csv', header=0, delimiter=',')
df_elevation = pd.read_csv(
    './Data/elevation/23-10-26_data_with_location_elevation.csv', header=0, delimiter=',')


df_elevation.drop(columns=["start_time", "end_time",
                  "duration", "user_id", "company"], inplace=True)
df_elevation.drop_duplicates(inplace=True)


df_rides['start_time'] = pd.to_datetime(df_rides['start_time'])
df_rides['end_time'] = pd.to_datetime(df_rides['end_time'])


df_rides['duration_min'] = (
    df_rides['end_time'] - df_rides['start_time']).dt.total_seconds() // 60
df_rides.drop(columns="duration", inplace=True)

# creation of join keys
df_rides['time-key'] = pd.to_datetime(df_rides['start_time']).dt.round("H")

df_weather['time-key'] = pd.to_datetime(df_weather['time'],
                                        format='mixed').dt.floor("H")


df_rides_weather = pd.merge(df_rides, df_weather, on="time-key", how="inner")

# filter out data too short or too long
df_rides_weather = df_rides_weather[(df_rides_weather['duration_min'] > 1) & (df_rides_weather['duration_min'] < 480)]


df_rides_weather_elevation = pd.merge(
    df_rides_weather, df_elevation, on=['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude'], how="inner")


#drop unnecessary columns
df_rides_weather_elevation.drop(columns=["time-key","time"])


df_rides_weather_elevation.to_csv(
    "./Data/merged/data_filtered_weather_elevation.csv", index=False)
