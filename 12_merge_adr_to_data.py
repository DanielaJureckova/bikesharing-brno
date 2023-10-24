import geopy        
import pandas as pd
import csv
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_distance(place1, place2):
    distance = geodesic(place1, place2).kilometers  
    return distance


trips = pd.read_csv("./data_brno/next_rekola_both.csv")

stations = pd.read_csv("stations_all.csv")
stations_list = stations.to_dict(orient='records')


trips["start_address"] = ""

index = 0

for row in range(len(trips)):
    s_lat = trips.loc[row, "start_latitude"]
    s_lon = trips.loc[row, "start_longitude"]
    e_lat = trips.loc[row, "end_latitude"]
    e_lon = trips.loc[row, "end_longitude"]

    for station in stations_list:
        distance_start = get_distance((s_lat, s_lon), (station["lat"], station["lgn"]))
        station["distance_start"] = distance_start
        distance_end = get_distance((e_lat, e_lon), (station["lat"], station["lgn"]))
        station["distance_end"] = distance_end
        
        
    
    min_distance_start = min(stations_list, key=lambda x: x["distance_start"])
    if min_distance_start["distance_start"] < 0.05:
        trips.loc[row, "start_address"] = min_distance_start["address"]
    else:
        trips.loc[row, "start_address"] = "N/A"

    
    min_distance_end = min(stations_list, key=lambda x: x["distance_end"])
    if min_distance_end["distance_end"] < 0.05:
        trips.loc[row, "end_address"] = min_distance_end["address"]
    else:
        trips.loc[row, "end_address"] = "N/A"

    
trips.to_csv("new_data.csv")




    
    

    




                         