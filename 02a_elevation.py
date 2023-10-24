import requests
import json

#get_altitude(): returns altitude from lat and lng
  
def get_altitude(lat, lng):
    response = requests.post(
                url="https://api.open-elevation.com/api/v1/lookup",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps({
                    "locations": [
                        {
                            "longitude": lng,
                            "latitude": lat
                        },
                    ]
                })
            )

    data = json.loads(response.content)

    altitude = data["results"][0]["elevation"]

    return altitude

#test sněžkou
print(get_altitude(50.7360, 15.7399))