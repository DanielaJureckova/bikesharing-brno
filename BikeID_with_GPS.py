import json
import pprint

bike_ids = set()

bike_places = dict()

with open("./json/response20230928-172959.json", mode="r", encoding="utf-8") as incoming_json:
    structured_file = json.load(incoming_json)
    city = structured_file['countries'][0]['cities'][0]
    print(city['name'])
    places = city['places']
    number_of_bikes = 0
    for place in places:
        if place['bike'] == True:
            print(place)
            print(" ")
            number_of_bikes += 1
            bike_id = place['bike_numbers'][0]
            bike_ids.add(bike_id)
            if (bike_id not in bike_places):
                bike_places[bike_id] = [(place['lat'], place['lng'])]
            else:
                bike_places[bike_id].append((place['lat'], place['lng']))
        else:
            number_of_bikes += int(place['bikes'])
            bikes_on_place = place['bike_list']
            for bike in bikes_on_place:
                bike_id = bike['number']
                bike_ids.add(bike_id)
                if (bike_id not in bike_places):
                    bike_places[bike_id] = [(place['lat'], place['lng'])]
                else:
                    bike_places[bike_id].append((place['lat'], place['lng']))

print(bike_ids)
print(f"pocet unikatnich 'ids' je : {len(bike_ids)}")
print(f"celkovy pocet kol je {number_of_bikes}")

pprint.pprint(bike_places)
