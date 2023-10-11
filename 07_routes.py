import openrouteservice
from openrouteservice import convert
from openrouteservice.directions import directions
import pprint
import json
import geopandas

coords = ((16.61304474,49.19127175),(16.59422636,49.21028027))

client = openrouteservice.Client(key='5b3ce3597851110001cf6248dc769df6350b4634869b55b7f7ef7e03') # Specify your personal API key
routes = directions(client,coordinates=coords, profile='cycling-regular')
geometry = routes['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)

pprint.pprint(routes)

print(decoded)

with open("07_routes_01_nextbike.json", mode="w", encoding="utf-8") as outputfile:
    json.dump(decoded, outputfile)