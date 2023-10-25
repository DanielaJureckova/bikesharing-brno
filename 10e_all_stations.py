import geopy        
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# calculates distance between two places, where place = (lat, lgn)
def get_distance(place1, place2):
    distance = geodesic(place1, place2).kilometers  
    return distance

# PART1: extract start and end locations from available datafiles and create one dataframe with duplicates(latitude and longitude) grouped
data_file = "next_rekola_both.csv"

trips = pd.read_csv(data_file, delimiter =",", decimal='.')

start_gps = trips[["start_latitude", "start_longitude"]]
start_gps = start_gps.rename(columns={"start_latitude": "latitude", "start_longitude": "longitude"})

end_gps = trips[["end_latitude", "end_longitude"]]
end_gps = end_gps.rename(columns={"end_latitude": "latitude", "end_longitude": "longitude"})


gps = pd.concat([start_gps, end_gps], ignore_index = True)
gps["latitude"] = gps["latitude"].round(4)
gps["longitude"] = gps["longitude"].round(4)

stations = gps.groupby(["latitude", "longitude"]).size().reset_index(name = "count")
print(stations)

stations["address"] = None

stations.to_csv("stations_from_all_data.csv", index = False)

# # PARt2 - add location to coordinates
# geolocator = Nominatim(user_agent="myGeocoder")

# n=0
# for row in range(800,820): 
#     latitude = float(stations.loc[row, "latitude"])
#     longitude = float(stations.loc[row, "longitude"])
#     location = geolocator.reverse(f"{latitude}, {longitude}")
#     stations.loc[row, "address"] = str(location)
#     n += 1
#     print(n)


# stations.to_csv("10e_stations_adr.csv", index = False)

# # # # PART3 agregation based on adresses

stations_df = pd.DataFrame(columns=["latitude", "lognitude", "count", "address"])


stations.sort_values(by='count', ascending=False, inplace = True)
stations.reset_index(inplace=True)

print(stations)

station_list = []

for index, row in stations.iterrows():
    latitude = row["latitude"]
    longitude = row["longitude"]
    count = row["count"]
    station_list.append([latitude, longitude, count])

index = 0
count = 0
station_list2 = station_list

for place1 in station_list:
    coordinates1 = (place1[0], place1[1])
    count += place1[2] 
    
    for place2 in station_list:
        coordinates2 = (place2[0],place2[1])
        if get_distance(coordinates1, coordinates2) < 0.05:
            station_list2[index] = [place1[0], place1[1], place2[2]]

        index += 1

    index = 0 

stations_df = pd.DataFrame(station_list2, columns = ['latitude', "longitude", "count"])
stations_final = stations_df.groupby(['latitude', "longitude"])["count"].sum()
stations_final_df = stations_final.reset_index()



stations_final_df.sort_values(by='count', ascending=False, inplace = True)

stations_final_df.to_csv("10e_stations_adr.csv", index = False)


