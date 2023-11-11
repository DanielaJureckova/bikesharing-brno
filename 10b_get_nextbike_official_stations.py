import pandas as pd
import requests

base_url = "https://maps.googleapis.com/maps/api/elevation/json"
api_key = "api-key"

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

data_file2022 = "data/2022/nextbike_22.csv"
data_file2023a = "data/2023/nextbike_23_08.csv"
data_file2023b = "data/2023/nextbike_23_09.csv"

nextbike_2022 = pd.read_csv(data_file2022, delimiter =";", decimal='.')

nextbike_2023a = pd.read_csv(data_file2023a, delimiter =",", decimal=',')
nextbike_2023b = pd.read_csv(data_file2023b, delimiter =",", decimal=',')

nextbike_2023 = pd.concat([nextbike_2023a, nextbike_2023b], ignore_index = True)

start22 = (nextbike_2022[["start_place", "start_lat", "start_lng"]])
start22 = (start22.rename(columns={ "start_place": "place", "start_lat": "latitude", "start_lng": "longitude"}))
 
end22 = (nextbike_2022[["end_place", "end_lat", "end_lng"]])
end22 = (end22.rename(columns={ "end_place": "place", "end_lat": "latitude", "end_lng": "longitude"}))

start23 = (nextbike_2023[["start_place", "start_latitude", "start_longitude"]])
start23 = (start23.rename(columns={"start_place": "place", "start_latitude": "latitude", "start_longitude": "longitude"}))

end23 = (nextbike_2023[["end_place", "end_latitude", "end_longitude"]])
end23 = (end23.rename(columns={"end_place": "place", "end_latitude": "latitude", "end_longitude": "longitude"}))

stations = pd.concat([start22, end22, start23, end23], ignore_index = True)

stations.latitude = stations.latitude.astype(str)
stations.longitude = stations.longitude.astype(str)

#převod desetinných čárek na desetinné tečky v lat, lng
stations.latitude = stations.latitude.str.replace(',', '.').astype(float)
stations.longitude = stations.longitude.str.replace(',', '.').astype(float)
stations.place = stations.place.str.strip()

stations = stations.dropna()

stations = stations.groupby("place").agg({'latitude': 'median', 'longitude': 'median'}).reset_index()
stations = stations[~stations["place"].str.startswith("BIKE")]
print(stations)
stations = stations.reset_index(drop=True)
print(stations)

stations['elevation'] = stations.apply(get_elevation, axis=1)

stations.to_csv("official_nextbike_stations.csv", index = False)



