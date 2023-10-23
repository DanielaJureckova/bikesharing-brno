
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
data_file2022 = "./data_brno/2022/rekol_2.csv"

rekola_2022 = pd.read_csv(data_file2022, delimiter =";", decimal=',')

start_gps = (rekola_2022[["start_latitude", "start_longitude"]])
start_gps = (start_gps.rename(columns={"start_latitude": "lat", "start_longitude": "lgn"}))

end_gps = (rekola_2022[["end_latitude", "end_longitude"]])
end_gps = (end_gps.rename(columns={"end_latitude": "lat", "end_longitude": "lgn"}))


data_file2023 = "./data_brno/2023/rekola_23.csv"

rekola_2023 = pd.read_csv(data_file2023, delimiter =";", decimal='.')

start_gps23 = rekola_2023[["start_latitude", "start_longitude"]]
start_gps23 = start_gps23.rename(columns={"start_latitude": "lat", "start_longitude": "lgn"})

end_gps23 = rekola_2023[["end_latitude", "end_longitude"]]
end_gps23 = end_gps23.rename(columns={"end_latitude": "lat", "end_longitude": "lgn"})


gps = pd.concat([start_gps, end_gps, start_gps23, end_gps23], ignore_index = True)

rekola_stations = gps.groupby(["lat", "lgn"]).size().reset_index(name = "count")


rekola_stations["address"] = None

rekola_stations.to_csv("rekola_gps_2223.csv")

# # PARt2 - add location to coordinates
file = "rekola_gps_2223.csv"
rekola_stations = pd.read_csv(file, delimiter =",", index_col=0)


geolocator = Nominatim(user_agent="myGeocoder")

n = 0
for row in range(23599, 28_829): 
    latitude = rekola_stations.loc[row, "lat"]
    longitude = rekola_stations.loc[row, "lgn"]

    location = geolocator.reverse(f"{latitude}, {longitude}")
    rekola_stations.loc[row, "address"] = str(location)
    to_print = [latitude, longitude, rekola_stations.loc[row, "count"], str(location)]
    with open("rekola_gps_with_adr.csv", mode = "a") as file:
        print(to_print, file = file)
    n += 1
   


# # PART3 agregation based on adresses



stations = pd.DataFrame(columns=["latitude", "lognitude", "count", "address"])

with open("rekola_gps_with_adr.csv", mode = "r") as file:
    for line in file:
        address = ", ".join(line.split(",")[3:-4])
        latitude = float(line.split(",")[0][1:])
        lognitude = float(line.split(",")[1])
        count = int(line.split(",")[2])
        new_row = [latitude, lognitude, count, address[2:]] 
        stations.loc[len(stations.index)] = new_row 


stations_grouped = stations.groupby("address").agg({'count': 'sum', 'latitude': 'mean',"lognitude":"mean"})
stations_sort = stations_grouped.sort_values(by='count', ascending=False)
stations_sort.reset_index(inplace=True)

print(stations_sort)

station_list = []

for index, row in stations_sort.iterrows():
    address = row['address']
    lat = row["latitude"]
    lgn = row["lognitude"]
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
stations_final = stations_df.groupby(['address', 'lat', "lgn"])["count"].sum()
stations_final_df = stations_final.reset_index()

stations_final.sort_values(ascending=False, inplace = True)


stations_final.to_csv("rekola_gps_csv.csv")





                              








