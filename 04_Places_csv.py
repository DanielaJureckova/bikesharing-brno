import json
import pprint
import csv

#exports uid and address of nextbike stations and their location as 
#lat and lng coordinates as .csv file in formate ["uid", "name", "lat" and "lgn"] 


#open and load
def stations_to_csv(input_json, output_csv):

    #open file
    with open(input_json, mode="r", encoding="utf-8") as json_file:
        all_data = json.load(json_file)
        places = all_data['countries'][0]['cities'][0]['places']

        #new list for data
        places_list = []

        #extracts official stations (not stand-alone bikes) and their id and locations
        for place in places:
            if "BIKE" not in place["name"]:
                station = [place["uid"], place["name"], place["lat"], place["lng"]]
                places_list.append(station)

    with open(output_csv, mode = "w", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        for row in places_list:
            writer.writerow(row)

#test
stations_to_csv("./json/response20230920-204422.json", "stations.csv")


