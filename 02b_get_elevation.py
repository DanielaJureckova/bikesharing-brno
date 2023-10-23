import requests

base_url = "https://maps.googleapis.com/maps/api/elevation/json"
api_key = #API key


# Specify the location (latitude and longitude) for which you want to get elevation
location = "49.192043,16.609182"  # Example location (New York City)

# Construct the full API request URL
url = f"{base_url}?locations={location}&key={api_key}"

# Send the HTTP GET request
response = requests.get(url)

# Parse the JSON response
data = response.json()

if data['status'] == 'OK':
    elevation = data['results'][0]['elevation']
    print(f"Elevation: {round(elevation)} meters")
else:
    print(f"Error: {data['status']}")




