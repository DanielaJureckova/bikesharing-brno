import pandas as pd
import datetime
import numpy as np

data22 = pd.read_csv('./Data/merged/next_rekola_22.csv', header=0, delimiter=',')
data23 = pd.read_csv('./Data/merged/next_rekola_23.csv', header=0, delimiter=',')

october23 = pd.read_csv('./Data/merged/next_rekola_23_october.csv', header=0, delimiter=',')

def append_data_of_23_dataset(inputDf):
    inputDf['start_time'] = pd.to_datetime(
        inputDf['start_time'], format='mixed')
    inputDf['end_time'] = pd.to_datetime(
        inputDf['end_time'], format='mixed')
    # inputDf['rok_s'] = pd.to_datetime(inputDf['start_time'], format='mixed').dt.year
    # inputDf['mesic_s'] = pd.to_datetime(inputDf['start_time'], format='mixed').dt.month
    # inputDf['den_s'] = pd.to_datetime(inputDf['start_time'], format='mixed').dt.dayofweek
    # inputDf['hodina_s'] = pd.to_datetime(inputDf['start_time'], format='mixed').dt.hour
    # inputDf['rok_k'] = pd.to_datetime(inputDf['end_time'], format='mixed').dt.year
    # inputDf['mesic_k'] = pd.to_datetime(inputDf['end_time'], format='mixed').dt.month
    # inputDf['den_k'] = pd.to_datetime(inputDf['end_time'], format='mixed').dt.dayofweek
    # inputDf['hodina_k'] = pd.to_datetime(inputDf['end_time'], format='mixed').dt.hour

# print(data23.dtypes)

append_data_of_23_dataset(data23)
# print(data23.dtypes)

# print(data23.head())

columns_22 = data22.columns
columns_23 = data23.columns
columns_23_october = october23.columns

# print(columns_22)
# print(columns_23)
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

print(columns_22_to_drop)
print(columns_23_to_drop)
data22.drop(columns=columns_22_to_drop, axis=1, inplace=True)

columns_to_check = ['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude']
for column in columns_to_check:
    data22[column] = data22[column].apply(lambda x: float(str(x).replace(',', '.')))
    data23[column] = data23[column].apply(lambda x: float(str(x).replace(',', '.')))
    october23[column] = october23[column].apply(lambda x: float(str(x).replace(',', '.')))

# data22.info()
# data23.info()
# october23.info()

frames = [data22, data23, october23]
result = pd.concat(frames)  

print(f"pocet pred dropovanim prazdnych: {len(result.index)} ")

for column in columns_to_check:
    result[column] = result[column].replace(0, np.nan)

result = result.dropna(subset=columns_to_check)

print(f"pocet podropovanim prazdnych: {len(result.index)} ")

# print(result.dtypes)

# rows_with_missing_values = result[result.isnull().any(axis=1)]
# print(rows_with_missing_values)

# print(frames)
result.to_csv("./Data/merged/next_rekola_all.csv", index=False)

#print(columns_22_to_drop)
#print(columns_23_to_drop)