import json

data = {}

with open("07_routes_01_nextbike.json", mode="r", encoding="utf-8") as input_file:
    data = json.load(input_file)

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": data
        }
    ]
}

with open('converted_data.json', mode='w') as outfile:
    json.dump(geojson, outfile, indent=4)

print("Data converted and saved to 'converted_data.json'")
