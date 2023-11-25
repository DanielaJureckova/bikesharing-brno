import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point

def find_nearest(gdA, gdB):
    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name="dist")
        ], 
        axis=1)
    return gdf

#data to gdf
stations = pd.read_csv("stations_data.csv")
stations["index"] = stations.index
stations["geometry"] = stations.apply(lambda row: Point(row.longitude, row.latitude), axis=1)
stations_gdf = gpd.GeoDataFrame(stations, geometry="geometry")

data = pd.read_csv("bike_rentals_data.csv")
data["geometry"] = data.apply(lambda row: Point(row.start_longitude, row.start_latitude), axis=1)
data_gdf = gpd.GeoDataFrame(data, geometry="geometry")

#assign start points
result_start_gdf = find_nearest(data_gdf, stations_gdf)
result_start_gdf = result_start_gdf.rename(columns={"street": "start_street", "address":"start_address", "elevation":"start_elevation", "index": "start_location", "dist": "start_dist"})
result_start_gdf.drop(columns=["count", "latitude", "longitude"], inplace = True)
result_start = result_start_gdf.drop(columns="geometry")

#assign end points

result_start["geometry2"] = result_start.apply(lambda row: Point(row.end_longitude, row.end_latitude), axis=1)
end_gdf = gpd.GeoDataFrame(result_start, geometry="geometry2")
result_end_gdf = find_nearest(end_gdf, stations_gdf)
result_end_gdf = result_end_gdf.rename(columns={"street": "end_street", "address":"end_address", "elevation":"end_elevation", "index": "end_location", "dist":"end_dist"})
result_end_gdf.drop(columns=["count", "latitude", "longitude"], inplace = True)
result_end = result_end_gdf.drop(columns="geometry2")

#export data
result_end.to_csv("data/name_of_merged_file.csv", index = False)




    
    

    




                         