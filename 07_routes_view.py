import folium
import json

data = {}
with open("07_routes_01_nextbike.json", mode="r", encoding="utf-8") as input_file:
    data = json.load(input_file)

map = folium.Map(location=[49.1913, 16.61302], zoom_start=15)

folium.GeoJson(data).add_to(map)

map.save("map.html")
