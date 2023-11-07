# import required modules
import os
import pandas as pd
import json
import csv
from datetime import datetime

#list for dataset
data = []
#data columns
data.append(["date", "time","uid", "lat", "lng", "bike", "name", "number", "booked_bikes", "bikes", "bike_types", "bike_number"])

 
number_of_col = len(data[0]) - 1

# assign directory
directory = 'json'
 
# iterate over files in directory
for filename in os.listdir(directory):

    #select json files
    if filename.endswith(".json"): 
        
        #extracting important information
        with open(("./json/"+filename), mode="r", encoding="utf-8") as file:
            file_content = json.load(file)
            city = file_content['countries'][0]['cities'][0]
            places = city['places']
            
            #date-time extraction
            date_format = datetime.strptime(filename[8:23], "%Y%m%d-%H%M%S")
            date = date_format.strftime("%Y-%m-%d")
            time = date_format.strftime("%H:%M:%S")

            #data extraction
            for place in places:
                single_data = [date, time]
                single_data.append(place["uid"])
                single_data.append(place["lat"])
                single_data.append(place["lng"])
                single_data.append(place["bike"])
                single_data.append(place["name"])
                single_data.append(place["number"])
                single_data.append(place["booked_bikes"])
                single_data.append(place["bikes"])
                single_data.append(place["bike_types"])
                if place["bike_numbers"] == []:
                    single_data.append(None)
                    data.append(single_data)
                    
                else:
                    for bike in place["bike_numbers"]:
                        single_data = single_data[:number_of_col]
                        single_data.append(bike)
                        data.append(single_data)
                        
                        


#save datafile                
with open("data.csv", mode = "w", encoding = "utf-8") as output_file:
    writer = csv.writer(output_file)
    for row in data:
        writer.writerow(row)



