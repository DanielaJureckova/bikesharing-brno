import os
import csv
import pandas as pd
import datetime

merge_22 = False
merge23 = True
renamingForNextBike = {'start_lat': "start_latitude",
                       "start_lng": "start_longitude",
                       'end_lat': "end_latitude",
                       "end_lng": "end_longitude",
                       'doration': "duration",
                       "customer": "user_id",
                       }


renamingForRekola = {"timediff": "duration",
                     "mesic_t_s": "mesic_s_t",
                     "mesic_t_k": "mesic_k_t"
                     }

renaming_for_next_bike_23 = {
    'duration_in_seconds': "duration", 'customer_id': 'user_id'}

renaming_for_rekola_23 = {'timediff': "duration"}


if merge_22:
    rekola22 = pd.read_csv(
        './Data/2022/rekola_22.csv', header=0, delimiter=';')
    nextBike22 = pd.read_csv(
        './Data/2022/nextbike_22.csv', header=0, delimiter=';')

    nextBike22.rename(renamingForNextBike, axis='columns', inplace=True)
    rekola22.rename(renamingForRekola, axis='columns', inplace=True)

    rekola22['company'] = 'rekola'
    nextBike22['company'] = 'nextbike'

    rekola22_columns = rekola22.columns
    nextBike22_columns = nextBike22.columns

    if rekola22['rental_id'].isnull().any():
        print('Existuji radky s NaN v sloupci rental_id')
        rekola22.dropna(subset=['rental_id'], inplace=True)
    else:
        print('neexistuji radky s NaN v sloupci rental_id')

    if len(rekola22_columns) != len(nextBike22_columns):
        print(
            f"neshoda v poctu sloupcu rekloa maji {len(rekola22_columns)} a nextbike maji {len(nextBike22_columns)}")

    # print(nextBike22_columns)
    # print(rekola22_columns)
    rekola_columns_to_drop = []
    for column in rekola22_columns:
        if column not in nextBike22_columns:
            rekola_columns_to_drop.append(column)
            print(f"sloupec co neni v nextBike je {column}")
    nextBike_columns_to_drop = []
    for column in nextBike22_columns:
        if column not in rekola22_columns:
            nextBike_columns_to_drop.append(column)
            print(f"sloupec co neni v rekola je {column}")

    nextBike22.drop(columns=nextBike_columns_to_drop, axis=1, inplace=True)
    rekola22.drop(columns=rekola_columns_to_drop, axis=1, inplace=True)

    if len(nextBike22.columns) == len(rekola22.columns):
        print(f"POG! Shoda v poctu sloupcu u obou datasetu")

    frames = [nextBike22, rekola22]
    result = pd.concat(frames)

    result['start_time'] = pd.to_datetime(
        result['start_time'], format='%d.%m.%Y %H:%M')
    
    result['end_time'] = pd.to_datetime(
        result['end_time'], format='%d.%m.%Y %H:%M')
    result.to_csv("./Data/merged/next_rekola_22.csv", index=False)


if merge23:
    rekola23 = pd.read_csv(
        './Data/2023/rekola_23.csv', header=0, delimiter=';')
    nextBike23 = pd.read_excel(
        './Data/2023/nextbike_23_09.xlsx')

    if len(rekola23.columns) != len(nextBike23.columns):
        print(
            f"neshoda v poctu sloupcu rekloa maji {len(rekola23.columns)} a nextbike maji {len(nextBike23.columns)}")

    nextBike23.rename(renaming_for_next_bike_23, axis='columns', inplace=True)
    rekola23.rename(renaming_for_rekola_23, axis='columns', inplace=True)

    rekola23['company'] = 'rekola'
    nextBike23['company'] = 'nextbike'

    rekola23_columns = rekola23.columns
    nextBike23_columns = nextBike23.columns

    rekola23_columns_to_remove = []
    for column in rekola23_columns:
        if column not in nextBike23_columns:
            rekola23_columns_to_remove.append(column)

    nextbike23_columns_to_remove = []
    for column in nextBike23_columns:
        if column not in rekola23_columns:
            nextbike23_columns_to_remove.append(column)

    print(rekola23_columns)
    print(nextBike23_columns)

    print(rekola23_columns_to_remove)
    print(nextbike23_columns_to_remove)

    nextBike23.drop(columns=nextbike23_columns_to_remove, axis=1, inplace=True)
    rekola23.drop(columns=rekola23_columns_to_remove, axis=1, inplace=True)

    if len(nextBike23.columns) == len(rekola23.columns):
        print(f"POG! Shoda v poctu sloupcu u obou datasetu")

    rekola23['start_time'] = pd.to_datetime(
        rekola23['start_time'], format='%d.%m.%Y %H:%M')

    nextBike23['start_time'] = pd.to_datetime(
        nextBike23['start_time'], format='%d.%m.%Y %H:%M')
    
    nextBike23['end_time'] = pd.to_datetime(
        nextBike23['end_time'], format='%d.%m.%Y %H:%M')
    
    rekola23['end_time'] = pd.to_datetime(
        rekola23['end_time'], format='%d.%m.%Y %H:%M')

    frames = [nextBike23, rekola23]
    result = pd.concat(frames)

    result.to_csv("./Data/merged/next_rekola_23.csv", index=False)

# print(nextBike22.columns)
# print(rekola22.columns)
