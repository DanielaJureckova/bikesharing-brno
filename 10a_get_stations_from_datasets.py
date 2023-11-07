
import geopy        
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests

base_url = "https://maps.googleapis.com/maps/api/elevation/json"
api_key = "api_key"
geolocator = Nominatim(user_agent="myNewGeocoder")

# calculates distance between two places, where place = (lat, lgn)
def get_distance(place1, place2):
    distance = geodesic(place1, place2).kilometers  
    return distance

def get_elevation(row):
    location = (str(row['latitude']) + "," + str(row['longitude']))
    url = f"{base_url}?locations={location}&key={api_key}"
    response = requests.get(url)

    data = response.json()
    if data['status'] == 'OK':
        elevation = data['results'][0]['elevation']
        return round(elevation)
    else:
        return "N/A"

# #rekola 

data_file2022 = "data/2022/rekola_22.csv"

rekola_2022 = pd.read_csv(data_file2022, delimiter =";", decimal=',')

start_gps = (rekola_2022[["start_latitude", "start_longitude"]])
start_gps = (start_gps.rename(columns={"start_latitude": "lat", "start_longitude": "long"}))

end_gps = (rekola_2022[["end_latitude", "end_longitude"]])
end_gps = (end_gps.rename(columns={"end_latitude": "lat", "end_longitude": "long"}))

print(len(start_gps))
print(len(end_gps))

data_file2023 = "data/2023/rekola_23.csv"

rekola_2023 = pd.read_csv(data_file2023, delimiter =";", decimal='.')

start_gps23 = rekola_2023[["start_latitude", "start_longitude"]]
start_gps23 = start_gps23.rename(columns={"start_latitude": "lat", "start_longitude": "long"})

end_gps23 = rekola_2023[["end_latitude", "end_longitude"]]
end_gps23 = end_gps23.rename(columns={"end_latitude": "lat", "end_longitude": "long"})

print(len(start_gps23))
print(len(end_gps23))

#nextbike
data_file2022 = "data/2022/nextbike_22.csv"
data_file2023a = "data/2023/nextbike_23_08.csv"
data_file2023b = "data/2023/nextbike_23_09.csv"

nextbike_2022 = pd.read_csv(data_file2022, delimiter =";", decimal='.')

nextbike_2023a = pd.read_csv(data_file2023a, delimiter =",", decimal=',')
nextbike_2023b = pd.read_csv(data_file2023b, delimiter =",", decimal=',')

nextbike_2023 = pd.concat([nextbike_2023a, nextbike_2023b], ignore_index = True)

start22 = (nextbike_2022[["start_lat", "start_lng"]])
start22 = (start22.rename(columns={ "start_lat": "lat", "start_lng": "long"}))
 
end22 = (nextbike_2022[["end_lat", "end_lng"]])
end22 = (end22.rename(columns={ "end_lat": "lat", "end_lng": "long"}))

start23 = (nextbike_2023[[ "start_latitude", "start_longitude"]])
start23 = (start23.rename(columns={"start_latitude": "lat", "start_longitude": "long"}))

end23 = (nextbike_2023[["end_latitude", "end_longitude"]])
end23 = (end23.rename(columns={"end_latitude": "lat", "end_longitude": "long"}))

print(len(start22))
print(len(end22))
print(len(start23))
print(len(end23))

gps = pd.concat([start22, end22, start23, end23, start_gps, end_gps, start_gps23, end_gps23], ignore_index = True)

gps.lat = gps.lat.astype(str)
gps.long = gps.long.astype(str)

#převod desetinných čárek na desetinné tečky v lat, lng
gps.lat = gps.lat.str.replace(',', '.').astype(float)
gps.long = gps.long.str.replace(',', '.').astype(float)


gps = gps.rename(columns = {'lat':'latitude', 'long':'longitude'} )

gps["latitude"] = gps["latitude"].round(4)
gps["longitude"] = gps["longitude"].round(4)

stations = gps.groupby(["latitude", "longitude"]).size().reset_index(name = "count")

stations["address"] = None

gps.to_csv("dataset.csv")

# PART2_agregation based on latitude/lognitude
stations.sort_values(by='count', ascending=False, inplace = True)
stations.reset_index(inplace=True)
print(stations.head())

station_list = []

for index, row in stations.iterrows():
    if (row["latitude"] < 90) and (row["longitude"] < 90):
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

stations_final_df.to_csv("yy-mm-dd__stations_grouped.csv", index = False)

stations = pd.read_csv("yy-mm-dd_stations_grouped.csv")

#tady to může zkolabovat, pokud nedostane rychlý response od serveru :) možno pustit zvlášť
for row in range(len(stations)): 
    latitude = float(stations.loc[row, "latitude"])
    longitude = float(stations.loc[row, "longitude"])
    location = geolocator.reverse(f"{latitude}, {longitude}")
    stations.loc[row, "address"] = str(location)

    street = (location.raw.get('address', {})).get('road')
    stations.loc[row, "street"] = street
    print(street)

stations.to_csv("yy-mm-dd__stations_streets.csv", index = False)

#PART4 - add elevation
stations = pd.read_csv("23-11-01_stations_streets.csv")

stations['elevation'] = stations.apply(get_elevation, axis=1)

stations.to_csv("yy-mm-dd__stations_all.csv", index = False)






