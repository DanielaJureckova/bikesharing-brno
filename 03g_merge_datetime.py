import pandas as pd
import numpy as np
df = pd.read_csv("Data/23-11-14_20-40_address_id.csv")

day_name_cz = {
    0: 'Pondělí', 1: 'Úterý', 2: 'Středa',
    3: 'Čtvrtek', 4: 'Pátek', 5: 'Sobota', 6: 'Neděle'
}

month_name_cz = {
    1: 'Leden', 2: 'Únor', 3: 'Březen', 4: 'Duben',
    5: 'Květen', 6: 'Červen', 7: 'Červenec', 8: 'Srpen',
    9: 'Září', 10: 'Říjen', 11: 'Listopad', 12: 'Prosinec'
}

df['start_time'] = pd.to_datetime(df['start_time'])

df["day_of_week"] = df["start_time"].dt.dayofweek
df['day_name_cz'] = df['day_of_week'].map(day_name_cz)
df['month_name_cz'] = df['month'].map(month_name_cz)

df["month_year"] = df["start_time"].dt.strftime('%m/%y')

# #unique addresses

# unique_addresses = df['start_address'].unique()

# unique_addresses = np.append(unique_addresses, df['end_address'].unique())

# unique_addresses = set(unique_addresses)

# unique_addresses = list(unique_addresses)

# df_address = pd.DataFrame(unique_addresses)

# df_address.index.name = "ID"
# df_address.columns = ['address']

# df_address = df_address.assign(row_number=range(len(df_address)))

# print("-----------------")

# df = df.merge(df_address, how='left', left_on='start_address', right_on='address')
# print(df.columns)
# df = df.rename(columns={"row_number": "start_address_id",})

# df = df.merge(df_address, how='left', left_on='end_address', right_on='address')

# df = df.rename(columns={"row_number": "end_address_id",})

# df_address.to_csv("./Data/merged/address.csv", index=True)

#unique place
unique_place = df['start_place'].unique()

unique_place = np.append(unique_place, df['end_place'].unique())

unique_place = set(unique_place)

unique_place = list(unique_place)

df_places = pd.DataFrame(unique_place)

df_places.index.name = "ID"
df_places.columns = ['place']

df_places = df_places.assign(place_id=range(len(df_places)))

print("-----------------")

df = df.merge(df_places, how='left', left_on='start_place', right_on='place')
print(df.columns)
df = df.rename(columns={"place_id": "start_place_id",})

df = df.merge(df_places, how='left', left_on='end_place', right_on='place')

df = df.rename(columns={"place_id": "end_place_id",})

df_places.to_csv("./Data/places.csv", index=True)

df.drop(columns=['start_place','end_place','place_x','place_y'], inplace=True)


df.to_csv("./Data/23-11-15_14-00_address_id.csv", index=False)