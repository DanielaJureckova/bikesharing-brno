import geopandas as gpd
import pandas as pd
import numpy as np

from scipy.spatial import cKDTree
from shapely.geometry import Point

def ckdnearest(gdA, gdB):

    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf

data_full = pd.read_csv("data/23-11-11_19_20_data_all.csv")
off_stations = pd.read_csv("official_stations_rekola_nextbike.csv")


#převedení na geodataframes

off_stations["index"] = off_stations.index
off_stations['geometry'] = off_stations.apply(lambda row: Point(row.longitude, row.latitude), axis=1)
stations_gdf = gpd.GeoDataFrame(off_stations, geometry='geometry')


data_full['geometry'] = data_full.apply(lambda row: Point(row.start_longitude, row.start_latitude), axis=1)
data_gdf = gpd.GeoDataFrame(data_full, geometry='geometry')

result_start_gdf = ckdnearest(data_gdf, stations_gdf)
result_start_gdf = result_start_gdf.rename(columns={'place': 'start_place', "dist": "start_dist", "nextbike": "start_nextbike", "rekola": "start_rekola"})
result_start_gdf.drop(columns=["latitude", "longitude", "elevation", "index"], inplace = True)

result_start = result_start_gdf.drop(columns='geometry')

result_start['geometry2'] = result_start.apply(lambda row: Point(row.end_longitude, row.end_latitude), axis=1)
end_gdf = gpd.GeoDataFrame(result_start, geometry='geometry2')

result_end_gdf = ckdnearest(end_gdf, stations_gdf)
result_end_gdf = result_end_gdf.rename(columns={'place': 'end_place', "dist":"end_dist", "nextbike": "end_nextbike", "rekola": "end_rekola"})
result_end_gdf.drop(columns=['latitude', 'longitude', "elevation", "index"], inplace = True)

new_data = result_end_gdf.drop(columns='geometry2')

new_data = new_data[['start_time', 'end_time', 'user_id', 'start_latitude',
       'start_longitude', 'end_latitude', 'end_longitude', 'company',
       'duration_min', 'temperature_2m (°C)', 'rain (mm)', 'snowfall (cm)',
       'wind_speed_10m (km/h)', 'wind_gusts_10m (km/h)', 'is_day ()', 'year',
       'month', 'day', 'hour', 'start_address', 'end_address', 'start_street',
       'end_street', 'start_location', 'end_location', 'start_elevation',
       'end_elevation', 'start_place','end_place', 'start_nextbike', 'start_rekola', 'end_nextbike', 'end_rekola', 'start_dist','end_dist']]

mask_st = new_data["start_dist"] > 0.0005
mask_en = new_data["end_dist"] > 0.0005

new_data.loc[mask_st, 'start_place'] = pd.NA
new_data.loc[mask_st, 'start_nextbike'] = pd.NA
new_data.loc[mask_st, 'start_rekola'] = pd.NA

new_data.loc[mask_en, 'end_place'] = pd.NA
new_data.loc[mask_en, 'end_nextbike'] = pd.NA
new_data.loc[mask_en, 'end_rekola'] = pd.NA

new_data.drop(columns=['start_dist', 'end_dist'], inplace = True)
new_data.rename(columns = {"start_place":"start_station", "end_place":"end_station"})

new_data.to_csv("23-11-11_20-20_data_all_oficial_stations.csv", index = False)