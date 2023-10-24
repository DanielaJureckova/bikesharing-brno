import requests
import pandas as pd

base_url = "https://maps.googleapis.com/maps/api/elevation/json"
api_key = #API key

stations = pd.read_csv("stations_all.csv")


def get_elevation(row):
    location = (str(row['lat']) + "," + str(row['lgn']))
    url = f"{base_url}?locations={location}&key={api_key}"
    response = requests.get(url)

    data = response.json()
    if data['status'] == 'OK':
        elevation = data['results'][0]['elevation']
        return round(elevation)
    else:
        return "N/A"

stations['elevation'] = stations.apply(get_elevation, axis=1)

stations.to_csv("stations_with_elev.csv", index = False)
