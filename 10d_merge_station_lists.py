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

#převedení na geodataframe:
nextbike = pd.read_csv("official_nextbike_stations.csv")
nextbike = nextbike[nextbike["latitude"]>49]
nextbike["index"] = nextbike.index
nextbike.columns = [col + "_n" for col in nextbike.columns] 
nextbike['geometry'] = nextbike.apply(lambda row: Point(row.longitude_n, row.latitude_n), axis=1)
nextbike_gdf = gpd.GeoDataFrame(nextbike, geometry='geometry')


rekola = pd.read_csv("official_rekola_stations.csv")
rekola.columns = [col + "_r" for col in rekola.columns] 
rekola['geometry'] = rekola.apply(lambda row: Point(row.longitude_r, row.latitude_r), axis=1)
rekola_gdf = gpd.GeoDataFrame(rekola, geometry='geometry')
result = ckdnearest(nextbike_gdf, rekola_gdf)
result = result.drop(columns='geometry')

mask = result["dist"] > 0.0003

result.loc[mask, ["place_r","latitude_r","longitude_r","elevation_r", "dist"]] = None

rekola_assigned = result[["place_r", "latitude_r", "longitude_r", "elevation_r"]].dropna()

rekola_not_assigned = pd.merge(rekola, rekola_assigned, on=['place_r'], how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
rekola_not_assigned = rekola_not_assigned.rename(columns = {'place_r_x':'place_r','latitude_r_x':'latitude_r', 'longitude_r_x':'longitude_r', "elevation_r_x": "elevation_r"} )

rekola_not_assigned = rekola_not_assigned[["place_r", "latitude_r", "longitude_r", "elevation_r"]].reset_index()

result_merged = pd.concat([result, rekola_not_assigned], axis = 0).drop(columns = ["index_n", "index"]).reset_index(drop=True)
result_merged["rekola"] = False
result_merged["nextbike"] = False

mask2 = (result_merged["latitude_n"].notna())&(result_merged["latitude_r"].notna())
result_merged.loc[mask2, "latitude"] = (result_merged["latitude_n"] + result_merged["latitude_r"])/2
result_merged.loc[mask2, "longitude"] = (result_merged["longitude_n"] + result_merged["longitude_r"])/2
result_merged.loc[mask2, "place"] = result_merged["place_n"] 
result_merged.loc[mask2, "elevation"] = (result_merged["elevation_n"] + result_merged["elevation_r"])/2
result_merged.loc[mask2, "rekola"] = True
result_merged.loc[mask2, "nextbike"] = True


mask3 = (result_merged["latitude_n"].notna())&(result_merged["latitude_r"].isna())
result_merged.loc[mask3, "latitude"] = result_merged["latitude_n"] 
result_merged.loc[mask3, "longitude"] = result_merged["longitude_n"] 
result_merged.loc[mask3, "place"] = result_merged["place_n"] 
result_merged.loc[mask3, "elevation"] = result_merged["elevation_n"] 
result_merged.loc[mask3, "nextbike"] = True

mask4 = (result_merged["latitude_r"].notna())&(result_merged["latitude_n"].isna())
result_merged.loc[mask4, "latitude"] = result_merged["latitude_r"] 
result_merged.loc[mask4, "longitude"] = result_merged["longitude_r"] 
result_merged.loc[mask4, "place"] = result_merged["place_r"] 
result_merged.loc[mask4, "elevation"] = result_merged["elevation_r"]
result_merged.loc[mask4, "rekola"] = True

result_merged["latitude"] = result_merged["latitude"].round(5)
result_merged["longitude"] = result_merged["longitude"].round(5)
result_merged["elevation"] = result_merged["elevation"].round(0)

result_final = result_merged[['place','latitude','longitude','elevation',"nextbike", "rekola"]]

result_final.to_csv("official_stations_rekola_nextbike.csv", index = False)




