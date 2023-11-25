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

data_full = pd.read_csv("data/23-11-17_19-00_address+places_id.csv")
data_full.drop(columns=["start_place_id", "end_place_id"], inplace = True)
off_stations = pd.read_csv("official_stations_rekola_nextbike.csv")



#převedení na geodataframes

off_stations["index"] = off_stations.index
off_stations['geometry'] = off_stations.apply(lambda row: Point(row.longitude, row.latitude), axis=1)
stations_gdf = gpd.GeoDataFrame(off_stations, geometry='geometry')


data_full['geometry'] = data_full.apply(lambda row: Point(row.start_longitude, row.start_latitude), axis=1)
data_gdf = gpd.GeoDataFrame(data_full, geometry='geometry')

result_start_gdf = ckdnearest(data_gdf, stations_gdf)
result_start_gdf = result_start_gdf.rename(columns={"dist": "start_dist", "place":"start_place"})
result_start_gdf.drop(columns=["latitude", "longitude", "elevation", "nextbike", "rekola", "index"], inplace = True)

result_start = result_start_gdf.drop(columns='geometry')

result_start['geometry2'] = result_start.apply(lambda row: Point(row.end_longitude, row.end_latitude), axis=1)
end_gdf = gpd.GeoDataFrame(result_start, geometry='geometry2')

result_end_gdf = ckdnearest(end_gdf, stations_gdf)
result_end_gdf = result_end_gdf.rename(columns={"dist":"end_dist", "place":"end_place" })
result_end_gdf.drop(columns=["latitude", "longitude", "elevation", "nextbike", "rekola", "index"], inplace = True)

new_data = result_end_gdf.drop(columns='geometry2')

new_data = new_data[['start_time', 'end_time', 'user_id', 'start_latitude',
       'start_longitude', 'end_latitude', 'end_longitude', 'company',
       'duration_min', 'temperature_2m (°C)', 'rain (mm)', 'snowfall (cm)',
       'wind_speed_10m (km/h)', 'wind_gusts_10m (km/h)', 'is_day ()', 'year',
       'month', 'day', 'hour', 'start_street', 'end_street', 'start_location',
       'end_location', 'start_elevation', 'end_elevation', 'elevation_dif',
       'day_of_week', 'day_name_cz', 'month_name_cz', 'month_year',
       'start_address_id', 'end_address_id','start_place','end_place', 'start_dist','end_dist', 'round_temperature']]


places = pd.read_csv("data/places.csv")
new_data_places1 = pd.merge(new_data, places, how = 'left', left_on = "start_place", right_on = "place")
new_data_places1 = new_data_places1.rename(columns={"place_id":"start_place_id"})
new_data_places1.drop(columns=["place", "ID"], inplace = True)


new_data_places = pd.merge(new_data_places1, places, how = 'left', left_on = "end_place", right_on = "place")
new_data_places = new_data_places.rename(columns={"place_id":"end_place_id"})

new_data_places.drop(columns=["place", "ID"], inplace = True)

#replace distant assignments with NA
mask_st = new_data_places["start_dist"] > 0.002
mask_en = new_data_places["end_dist"] > 0.002

new_data_places.loc[mask_st, 'start_place'] = pd.NA
new_data_places.loc[mask_st, 'start_place_id'] = pd.NA

new_data_places.loc[mask_en, 'end_place'] = pd.NA
new_data_places.loc[mask_en, 'end_place_id'] = pd.NA

new_data_places.drop(columns=['start_dist', 'end_dist'], inplace = True)

new_data_places = new_data_places[['start_time', 'end_time', 'user_id', 'start_latitude',
       'start_longitude', 'end_latitude', 'end_longitude', 'company',
       'duration_min', 'temperature_2m (°C)', 'rain (mm)', 'snowfall (cm)',
       'wind_speed_10m (km/h)', 'wind_gusts_10m (km/h)', 'is_day ()', 'year',
       'month', 'day', 'hour', 'start_street', 'end_street', 'start_location',
       'end_location', 'start_elevation', 'end_elevation', 'elevation_dif',
       'day_of_week', 'day_name_cz', 'month_name_cz', 'month_year',
       'start_address_id', 'end_address_id', 'start_place_id', 'end_place_id',
       'round_temperature']]


new_data_places.to_csv("23-11-18_15-30_adresses_places_id.csv", index = False)
