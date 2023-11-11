import pandas as pd
import requests

base_url = "https://maps.googleapis.com/maps/api/elevation/json"
api_key = "api_key"

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

stations = pd.read_csv("data/2023/Rekola_stanoviste_13-10-2023.csv")
stations.fillna("nespecifikováno", inplace=True)


stations["place"] = stations["name"] + " - " + stations["description"]


stations = stations.drop(["name","description", "image_url", "id"], axis = 1).reset_index(drop = True)

stations['elevation'] = stations.apply(get_elevation, axis=1)

stations = stations[["place", "latitude", "longitude", "elevation"]]

stations.to_csv("official_rekola_stations.csv", index = False)