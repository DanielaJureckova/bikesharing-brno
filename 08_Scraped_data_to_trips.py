import pandas as pd
import csv


data_file = "data.csv"

#get all bikes
bikes_data = pd.read_csv(data_file)
list_of_bikes = bikes_data["bike_number"].dropna().unique()
list_of_bikes = [int(x) for x in list_of_bikes]
    

#extract data of trips
trips = []
trips.append(["bike", "start-date", "start_time", "end_date", "end_time", "from_name", "from_uid", "from_lat", "from_lgn", "to_name", "to_uid", "to_lat", "to_lgn"])

#iterates over all available bikes and information about the trips is extracted
for bike in list_of_bikes:
    #extract and sort data about single bike
    bike_in_days = bikes_data[bikes_data["bike_number"] == bike][["date", "time","uid", "lat", "lng", "name", "bike_number"]]
    bike_in_days["bike_number"] = bike_in_days["bike_number"].astype(int)
    bike_in_days_sorted = bike_in_days.sort_values(by = ["date", "time"], ascending=[True, True])
    bike_in_days_sorted.reset_index(drop=True, inplace=True)

    #clean list: only rows, in those change in location (=uid) is observed is preserved:
    bikes_subset = ["uid"]
    bikes_short = bike_in_days_sorted[bikes_subset].where(bike_in_days_sorted[bikes_subset].ne(bike_in_days_sorted[bikes_subset].shift()))
    bikes_short2 = bike_in_days_sorted[bikes_subset].where(bike_in_days_sorted[bikes_subset].ne(bike_in_days_sorted[bikes_subset].shift(-1)))

    bikes_short.dropna(subset = "uid", inplace = True)
    bikes_short2.dropna(subset = "uid", inplace = True)
    bikes_all = pd.concat([bikes_short, bikes_short2], ignore_index=False)
    trip_data = pd.merge(bikes_all, bike_in_days_sorted, left_index=True, right_index=True, how='inner')
    trip_data = trip_data.sort_index()
    trip_data.reset_index(inplace=True)

    #transform the data into trips
    for i in range((len(trip_data)-1)):
        
        if trip_data.loc[i, "uid_y"] != trip_data.loc[(i+1), "uid_y"]:
            if trip_data.loc[i, "name"] != trip_data.loc[(i+1), "name"]:
                trip = []
                trip.append(trip_data.loc[i, "bike_number"])
                trip.append(trip_data.loc[i, "date"])
                trip.append(trip_data.loc[i, "time"])
                trip.append(trip_data.loc[(i+1), "date"])
                trip.append(trip_data.loc[(i+1), "time"])
                trip.append(trip_data.loc[i, "name"])
                trip.append(trip_data.loc[i, "uid_y"])
                trip.append(trip_data.loc[i, "lat"])
                trip.append(trip_data.loc[i, "lng"])
                trip.append(trip_data.loc[(i+1), "name"])
                trip.append(trip_data.loc[(i+1), "uid_y"])
                trip.append(trip_data.loc[(i+1), "lat"])
                trip.append(trip_data.loc[(i+1), "lng"])
                trips.append(trip)

#save trips to csv file
with open("trips.csv", 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write each row to the CSV file
    for row in trips:
        csv_writer.writerow(row)
    
    

