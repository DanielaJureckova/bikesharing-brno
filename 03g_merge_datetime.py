import pandas as pd
import numpy as np

df = pd.read_csv("Data/merged/23-11-14_20-40_address_id.csv")

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
