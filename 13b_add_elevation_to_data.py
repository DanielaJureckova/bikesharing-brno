import pandas as pd

dataset = pd.read_csv("merged_data_with_locations.csv")
stations = pd.read_csv("stations_with_elev.csv")

dataset1 = dataset.merge(stations[["address", "elevation"]], left_on = "start_address", right_on = "address", right_index=False, how = "left")
dataset1.drop('address', axis=1, inplace=True)
dataset1.rename(columns = {"elevation":"start_elevation"})

dataset2 = dataset1.merge(stations[["address", "elevation"]], left_on = "end_address", right_on = "address", right_index=False, how = "left")
dataset2.drop('address', axis=1, inplace=True)
dataset2.rename(columns = {"elevation":"end_elevation"})


dataset1.to_csv("data_test.csv", index=False)



