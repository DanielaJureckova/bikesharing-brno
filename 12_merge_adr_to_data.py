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
                           (station['latitude'], station['longitude'])).kilometers
        if distance < min_distance:
            min_distance = distance
            if min_distance < 0.05:
                start_location = station['station_index']
            else:
                start_location = "N/A"
                
    return start_location

def find_end_location(row):
    min_distance = float('inf')
    end_location = None
    for station in stations:
        distance = geodesic((row['end_latitude'], row['end_longitude']),
                           (station['latitude'], station['longitude'])).kilometers
        if distance < min_distance:
            min_distance = distance
            if min_distance < 0.10:
                end_location = station['station_index']
            else:
                end_location = "N/A"
                
    return end_location

trips = pd.read_csv("next_rekola_both.csv")

stations_all = pd.read_csv("10e_stations_ad_el.csv")
stations_all['station_index'] = stations_all.index

stations = stations_all.to_dict(orient='records')

# Přiřazení nejbližšího indexu lokality k GPS souřadnicím
trips['start_location'] = trips.apply(find_start_location, axis=1)
trips['end_location'] = trips.apply(find_end_location, axis=1)


trips.to_csv("23-10-25_data_merged_adr.csv", index = False)




    
    

    




                         