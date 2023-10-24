#join all station-dataset (nextbike, rekola and free nextbike bikes)

import geopy        
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

#calculates distance between two places, where place = (lat, lgn)
def get_distance(place1, place2):
    distance = geodesic(place1, place2).kilometers  
    return distance

rekola = pd.read_csv("rekola_stations_final.csv")

nextbike = pd.read_csv("nextbike_stations_with_adr.csv")
nextbike = nextbike.rename(columns={"lng": "lgn"})

nextbike_bikes = pd.read_csv("nxbike_bikes_stations.csv")

joined = pd.concat([nextbike, nextbike_bikes])

station_list = []

for index, row in joined.iterrows():
    address = row['address']
    lat = row["lat"]
    lgn = row["lgn"]
    count = row["count"]
    station_list.append([address, lat, lgn, count])

index = 0
count = 0
station_list2 = station_list

for place1 in station_list:
    coordinates1 = (place1[1], place1[2])
    count += place1[3]
    
    for place2 in station_list:
        coordinates2 = (place2[1],place2[2])
        if get_distance(coordinates1, coordinates2) < 0.06:
            station_list2[index] = [place1[0], place1[1], place1[2], place2[3]]
        index += 1

    index = 0 


stations_df = pd.DataFrame(station_list2, columns = ['address', 'lat', "lgn", "count"])
stations_final = stations_df.groupby(['address']).agg({'count': 'sum', 'lat': 'median',"lgn":"median"})
stations_final_df = stations_final.reset_index()
stations_final_df.sort_values(by = ["count"], ascending=False, inplace = True)


stations_final_df.to_csv("stations_all2.csv", index = False)






