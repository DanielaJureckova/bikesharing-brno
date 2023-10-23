#get and merge data from nextbike datasets: stations of nextbike bikes which are not in the official station

import geopy        
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_distance(place1, place2):
    distance = geodesic(place1, place2).kilometers  
    return distance

data_file2022 = "./data_brno/2022/nextbike_dash_2.csv"
data_file2023a = "./data_brno/2023/nextbike_23_08.csv"
data_file2023b = "./data_brno/2023/nextbike_23_09.csv"

nextbike_2022 = pd.read_csv(data_file2022, delimiter =";", decimal='.')

nextbike_2023a = pd.read_csv(data_file2023a, delimiter =",", decimal=',')
nextbike_2023b = pd.read_csv(data_file2023b, delimiter =",", decimal=',')

nextbike_2023 = pd.concat([nextbike_2023a, nextbike_2023b], ignore_index = True)

start22 = (nextbike_2022[["start_place", "start_lat", "start_lng"]])
start22 = (start22.rename(columns={"start_place": "place", "start_lat": "lat", "start_lng": "lng"}))
 
end22 = (nextbike_2022[["end_place", "end_lat", "end_lng"]])
end22 = (end22.rename(columns={"end_place": "place", "end_lat": "lat", "end_lng": "lng"}))

start23 = (nextbike_2023[["start_place", "start_latitude", "start_longitude"]])
start23 = (start23.rename(columns={"start_place": "place", "start_latitude": "lat", "start_longitude": "lng"}))

end23 = (nextbike_2023[["end_place", "end_latitude", "end_longitude"]])
end23 = (end23.rename(columns={"end_place": "place", "end_latitude": "lat", "end_longitude": "lng"}))

all = pd.concat([start22, end22, start23, end23], ignore_index = True)
all["count"] = 1 

#převod desetinných čárek na desetinné tečky v lat, lng
all.lat = all.lat.str.replace(',', '.').astype(float)
all.lng = all.lng.str.replace(',', '.').astype(float)


all= all[all["place"].str.startswith("BIKE")] 
all = all[all["lat"].notna()]
all = all[(all["lat"] > 1) &(all["lat"] < 50)]

bikes = all.groupby(["lat", "lng"]).size().reset_index(name = "count")

bikes["address"] = None

print(bikes.info())
# PARt2 - add location to coordinates

geolocator = Nominatim(user_agent="myGeocoder")

n=0
for row in range(len(bikes)): 
    latitude = float(bikes.loc[row, "lat"])
    longitude = float(bikes.loc[row, "lng"])
    location = geolocator.reverse(f"{latitude}, {longitude}")
    address = str(location)
    bikes.loc[row, "address"] = (",".join(address.split(",")[:-4]))
    n += 1
    print(n)

bikes.to_csv("bikes_with_adr", index = False)


stopped_bikes = pd.read_csv("bikes_with_adr.csv")

stopped_bikes = stopped_bikes.groupby("address").agg({'count': 'sum', 'lat': 'median',"lng":"median"})
bikes_sorted = stopped_bikes.sort_values(by='count', ascending=False)
bikes_sorted.reset_index(inplace=True)


bikes_list = []

for index, row in bikes_sorted.iterrows():
    address = row['address']
    lat = row["lat"]
    lgn = row["lng"]
    count = row["count"]
    bikes_list.append([address, lat, lgn, count])

index = 0
count = 0
bikes_list2 = bikes_list

for place1 in bikes_list:
    coordinates1 = (place1[1], place1[2])
    count += place1[3] #?
    
    for place2 in bikes_list:
        coordinates2 = (place2[1],place2[2])
        if get_distance(coordinates1, coordinates2) < 0.06:
            bikes_list2[index] = [place1[0], place1[1], place1[2], place2[3]]

        index += 1

    index = 0 

stations_df = pd.DataFrame(bikes_list2, columns = ['address', 'lat', "lgn", "count"])
stations_final = stations_df.groupby(['address', 'lat', "lgn"])["count"].sum()
stations_final_df = stations_final.reset_index()

stations_final.sort_values(ascending=False, inplace = True)
stations_final.to_csv("nxbike_bikes_stations.csv")
