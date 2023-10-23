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


data22.drop(columns=columns_22_to_drop, axis=1, inplace=True)

# print(data22)

columns_to_convert = ['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude']
for column in columns_to_convert:
    data22[column] = data22[column].apply(lambda x: float(str(x).replace(',', '.')))
    data23[column] = data23[column].apply(lambda x: float(str(x).replace(',', '.')))

# print(data23.dtypes)
# print(data23)

# data22.info()
# data23.info()

frames = [data22, data23]
result = pd.concat(frames)  
result = result.dropna(subset=['start_longitude'])


# print(result.dtypes)

# rows_with_missing_values = result[result.isnull().any(axis=1)]
# print(rows_with_missing_values)

# print(frames)
result.to_csv("./Data/merged/next_rekola_both.csv", index=False)

#print(columns_22_to_drop)
#print(columns_23_to_drop)