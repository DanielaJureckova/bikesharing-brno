import geopy        
import pandas as pd
import csv
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


# addition of the closest start/end station (address) to each row, exact gps
# v datech manuální edit na řádku 153307: upravena lat z 49183.0 na 49.183

def get_distance(place1, place2):
    distance = geodesic(place1, place2).kilometers  
    return distance

def find_start_location(row):
    min_distance = float('inf')
    start_location = None
    for station in stations:
        distance = geodesic((row['start_latitude'], row['start_longitude']),
                           (station['lat'], station['lgn'])).kilometers
        if distance < min_distance:
            min_distance = distance
            if min_distance < 0.05:
                start_location = station['Unnamed: 0']
            else:
                start_location = "N/A"
                
    return start_location

def find_end_location(row):
    min_distance = float('inf')
    end_location = None
    for station in stations:
        distance = geodesic((row['end_latitude'], row['end_longitude']),
                           (station['lat'], station['lgn'])).kilometers
        if distance < min_distance:
            min_distance = distance
            if min_distance < 0.10:
                end_location = station['Unnamed: 0']
            else:
                end_location = "N/A"
                
    return end_location

trips = pd.read_csv("next_rekola_both.csv")

stations_all = pd.read_csv("stations_with_elev.csv")

stations = stations_all.to_dict(orient='records')


# Přiřazení nejbližšího názvu lokality k GPS souřadnicím
trips['start_location'] = trips.apply(find_start_location, axis=1)
trips['end_location'] = trips.apply(find_end_location, axis=1)


trips.to_csv("data_with_addresses2.csv", index = False)




    
    

    




                         