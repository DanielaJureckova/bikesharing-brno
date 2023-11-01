from geopy.geocoders import Nominatim
import pandas as pd

stations = pd.read_csv("10e_stations_ad_el.csv")

geolocator = Nominatim(user_agent="myGeocoder")


for row in range(len(stations)): 
    latitude = float(stations.loc[row, "latitude"])
    longitude = float(stations.loc[row, "longitude"])
    location = geolocator.reverse(f"{latitude}, {longitude}")
    address = location.raw.get('address', {})
    street = address.get('road')
    stations.loc[row, "street"] = street
 

stations.to_csv("stations_adr_str_el.csv", index=False)