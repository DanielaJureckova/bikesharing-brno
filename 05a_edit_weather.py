import pandas as pd
import math
df = pd.read_csv("Data/merged/23-11-16_20-25_address+places_id.csv")

df['round_temperature'] = round(df['temperature_2m (°C)']) 


df.to_csv("./Data/23-11-17_19-00_address+places_id.csv", index=False)