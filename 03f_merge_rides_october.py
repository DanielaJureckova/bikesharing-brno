import pandas as pd 

renaming_for_rekola_23_october = {'timediff': "duration"}

renaming_for_next_bike_23_october = {
    'duration_in_seconds': "duration", 'customer_id': 'user_id'}

rekola23_october = pd.read_csv('Data/2023-10/rekola_10.csv', header=0, delimiter=',')
nextBike23_october = pd.read_csv('Data/2023-10/nextbike_10.csv', header=0, delimiter=',')

rekola23_october.rename(renaming_for_rekola_23_october, axis='columns', inplace=True)
nextBike23_october.rename(renaming_for_next_bike_23_october, axis='columns', inplace=True)

rekola23_october['company'] = 'rekola'
nextBike23_october['company'] = 'nextbike'

rekola23_october_columns = rekola23_october.columns
nextBike23_october_columns = nextBike23_october.columns

print(f"pocet pred rekola 23 october: {len(rekola23_october.index)} ")
print(f"pocet pred nextbike 23 october: {len(nextBike23_october.index)} ")

#remove columns
rekola23_october_columns_to_remove = []
for column in rekola23_october_columns:
    if column not in nextBike23_october_columns:
        rekola23_october_columns_to_remove.append(column)

nextbike23_october_columns_to_remove = []
for column in nextBike23_october_columns:
    if column not in rekola23_october_columns:
        nextbike23_october_columns_to_remove.append(column)

rekola23_october.drop(columns=rekola23_october_columns_to_remove, axis=1, inplace=True)
nextBike23_october.drop(columns=nextbike23_october_columns_to_remove, axis=1, inplace=True)

# if len(rekola23_october.columns) == len(nextBike23_october.columns):
#     print(f"POG! Shoda v poctu sloupcu u obou datasetu")

rekola23_october['start_time'] = pd.to_datetime(
    rekola23_october['start_time'], format='%Y-%m-%dT%H:%M:%S')

nextBike23_october['start_time'] = pd.to_datetime(
    nextBike23_october['start_time'], format='%m/%d/%Y %H:%M')
    
rekola23_october['end_time'] = pd.to_datetime(
    rekola23_october['end_time'], format='%Y-%m-%dT%H:%M:%S')
    
nextBike23_october['end_time'] = pd.to_datetime(
    nextBike23_october['end_time'], format='%m/%d/%Y %H:%M')


columns_to_check = ['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude']
for column in columns_to_check:
    nextBike23_october[column] = nextBike23_october[column].apply(lambda x: str(x).replace(',', ''))
    nextBike23_october[column] = nextBike23_october[column].apply(lambda x: float(x[:2] + "." + x[2:]))

print(f"pocet po rekola 23 october: {len(rekola23_october.index)} ")
print(f"pocet po nextbike 23 october: {len(nextBike23_october.index)} ")

frames = [rekola23_october, nextBike23_october]
result = pd.concat(frames)

result.to_csv("./Data/merged/next_rekola_23_october.csv", index=False)