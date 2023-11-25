#get elevation using google maps API

import requests

base_url = "https://maps.googleapis.com/maps/api/elevation/json"
api_key = "inser API key here"
location = "insert location"  

url = f"{base_url}?locations={location}&key={api_key}"
response = requests.get(url)
data = response.json()

if data['status'] == 'OK':
    elevation = data['results'][0]['elevation']
    print(f"Elevation: {round(elevation)} meters")
else:
    print(f"Error: {data['status']}")




