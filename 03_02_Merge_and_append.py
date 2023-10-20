import pandas as pd
import datetime

data22 = pd.read_csv(
    './Data/merged/next_rekola_22.csv', header=0, delimiter=',')
data23 = pd.read_csv(
    './Data/merged/next_rekola_23.csv', header=0, delimiter=',')


def append_data_of_23_dataset(inputDf):
    inputDf['start_time'] = pd.to_datetime(
        inputDf['start_time'], format='mixed')
    inputDf['end_time'] = pd.to_datetime(
        inputDf['end_time'], format='mixed')
    inputDf['rok_s'] = pd.to_datetime(inputDf['start_time'], format='mixed').dt.year
    inputDf['mesic_s'] = pd.to_datetime(inputDf['start_time'], format='mixed').dt.month
    inputDf['den_s'] = pd.to_datetime(inputDf['start_time'], format='mixed').dt.dayofweek
    inputDf['hodina_s'] = pd.to_datetime(inputDf['start_time'], format='mixed').dt.hour
    inputDf['rok_k'] = pd.to_datetime(inputDf['end_time'], format='mixed').dt.year
    inputDf['mesic_k'] = pd.to_datetime(inputDf['end_time'], format='mixed').dt.month
    inputDf['den_k'] = pd.to_datetime(inputDf['end_time'], format='mixed').dt.dayofweek
    inputDf['hodina_k'] = pd.to_datetime(inputDf['end_time'], format='mixed').dt.hour

#print(data23.dtypes)

append_data_of_23_dataset(data23)
print(data23.dtypes)

print(data23.head())

columns_22 = data22.columns
columns_23 = data23.columns

print(columns_22)
print(columns_23)
columns_22_to_drop = []
for column in columns_22:
    if column not in columns_23:
        columns_22_to_drop.append(column)
        print(f"sloupec co neni v roce 23 je {column}")
columns_23_to_drop = []
for column in columns_23:
    if column not in columns_22:
        columns_23_to_drop.append(column)
        print(f"sloupec co neni v roce 22 je {column}")



data22.drop(columns=columns_22_to_drop, axis=1, inplace=True)


frames = [data22, data23]
result = pd.concat(frames)   


result.to_csv("./Data/merged/next_rekola_both.csv")

#print(columns_22_to_drop)
#print(columns_23_to_drop)
