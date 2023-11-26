# extracts all latitude/longitude coordinates from rekola/nextbike 22/23 datasets and groups them together, adds elevation and street/address of location 
      
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests

base_url = "https://maps.googleapis.com/maps/api/elevation/json"
api_key = "api key"

geolocator = Nominatim(user_agent="myNewGeocoder")

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

# PART1: extract start and end locations from available datafiles and create one dataframe with duplicates(latitude and longitude) grouped
data_file = "data/data_file_with_start_end_gps.csv"

trips = pd.read_csv(data_file, delimiter =",", decimal='.')

start_gps = trips[["start_latitude", "start_longitude"]]
start_gps = start_gps.rename(columns={"start_latitude": "latitude", "start_longitude": "longitude"})

end_gps = trips[["end_latitude", "end_longitude"]]
end_gps = end_gps.rename(columns={"end_latitude": "latitude", "end_longitude": "longitude"})


gps = pd.concat([start_gps, end_gps], ignore_index = True)
gps["latitude"] = gps["latitude"].round(4)
gps["longitude"] = gps["longitude"].round(4)
stations = gps.groupby(["latitude", "longitude"]).size().reset_index(name = "count")

stations["address"] = None


# PART2_agregation based on latitude/lognitude
stations.sort_values(by='count', ascending=False, inplace = True)
stations.reset_index(inplace=True)

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

stations_final_df.to_csv("data_results01.csv", index = False)


# PARt3 - add location to coordinates
# Note: could potentially collapse, when server response is too slow
stations = pd.read_csv("data_results01.csv.csv")

index = 0
for row in range(len(stations)): 
    latitude = float(stations.loc[row, "latitude"])
    longitude = float(stations.loc[row, "longitude"])
    location = geolocator.reverse(f"{latitude}, {longitude}")
    stations.loc[row, "address"] = str(location)

    street = (location.raw.get('address', {})).get('road')
    stations.loc[row, "street"] = street
    index +=1
    print(street)
    print(index)

#PART4 - add elevation
stations['elevation'] = stations.apply(get_elevation, axis=1)

stations.to_csv("output_file.csv", index = False)


