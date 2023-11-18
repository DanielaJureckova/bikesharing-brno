import streamlit as st
import pandas as pd
import time 
import plotly.express as px
import matplotlib.pyplot as plt

from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl

#page config
st.set_page_config(
    page_title="Bikesharing Brno",
    page_icon="🚲",
    layout="wide",
)

#data
stations = pd.read_csv("data/23-11-18_17-19_stations_occupancy.csv")
official = pd.read_csv("official_nextbike_stations.csv")
official["station_id"] = official.index

stations["date-time"] = pd.to_datetime(stations["date-time"], format="%Y-%m-%d %H:%M:%S", errors = "coerce")


#filtering
hour_range = st.sidebar.slider("Vyber hodinu", 0, 23, (0, 23))
start_hour, end_hour = hour_range

filtered_h_data = stations[
    (stations["date-time"].dt.hour >= start_hour) & (stations["date-time"].dt.hour <= end_hour)]


day_type = st.sidebar.selectbox("víkend vs. všední dny", ["víkendy", "všední dny", "vše"])


# Filtr podle vybraného typu dne
if day_type == "všední dny":
    data_filtered = filtered_h_data[filtered_h_data['date-time'].dt.dayofweek < 5]  
elif day_type == 'Víkendy':
    data_filtered = filtered_h_data[filtered_h_data['date-time"'].dt.dayofweek >= 5]  # 5-6 reprezentuje sobotu a neděli
else:
    data_filtered = filtered_h_data  # Zobrazí všechny dny



average_occupancy_1_0 = data_filtered[["station_id", "occupancy"]].groupby(by = "station_id").mean()

station_avg_occ = average_occupancy_1_0.sort_values(by="occupancy", ascending=True)
occ_and_elev = pd.merge(station_avg_occ, official, on='station_id', how='inner')


#page
st.subheader("Obsazenost stanic společnosti Nextbike")

st.write("Průměrná obsazenost stanic společnosti Nextbike v období 21.9.2023 - 09.11.2023.")
st.markdown("---")


col2_spacer0, col2_1, col2_spacer1, col2_2, col2_spacer2, col2_3, col2_spacer3   = st.columns((1, 1.5, 0.2, 0.5, .2, 2, .2))

occ_90more = occ_and_elev[occ_and_elev['occupancy']>0.9]
occ_20less = occ_and_elev[occ_and_elev['occupancy']<0.2]
occ_50more = occ_and_elev[occ_and_elev['occupancy']>0.5]

with col2_1:
    st.write("📍")
    st.write("Celkový počet stanic")
    st.write("Stanice s obsazeností > 90%")
    st.write("Stanice s obsazeností > 50%")
    st.write("Stanice s obsazeností < 20%")

with col2_2:
    st.write("počet")
    st.write(str(len(occ_and_elev)))
    st.write(str(len(occ_90more)))
    st.write(str(len(occ_50more)))
    st.write(str(len(occ_20less)))


with col2_3:
    st.write("průměrná nadmořská výška")
    st.write(str(int(occ_and_elev['elevation'].mean())) + " m.n.m.")
    st.write(str(int(occ_90more['elevation'].mean())) + " m.n.m.")
    st.write(str(int(occ_50more['elevation'].mean()))+ " m.n.m.")
    st.write(str(int(occ_20less['elevation'].mean()))+ " m.n.m.")
st.markdown("---")
st.subheader("Obsazenost vybrané stanice:")
col3_spacer0, col3_1, col3_spacer1, col3_2, col3_spacer1 = st.columns((.2, 3, 1, 3, 0.2))

with col3_1:
    sel_place = st.selectbox("Vyber stanici:", occ_and_elev["place"], label_visibility = "hidden" )
value = round((occ_and_elev.loc[occ_and_elev['place'] == sel_place, 'occupancy'].values[0]*100), 2)
with col3_2:
  st.metric("Obsazenost:", f"{value} %", label_visibility="hidden")

st.markdown("---")

st.subheader("Mapa obsazenosti:")

row4_spacer0, row4_1, row4_spacer1, row4_2, row4_spacer2   = st.columns((.2, 3, 1, 3, 0.2))
with row4_1:
    occupancy_set = st.slider("Rozsah obsazenosti (%):", 0, 100, (0,100),)
occupancy_set_low = occupancy_set[0]/100
occupancy_set_high = occupancy_set[1]/100 
occupancy_dif = occupancy_set[1] - occupancy_set[0]

data_kepler = occ_and_elev[(occ_and_elev["occupancy"]>=occupancy_set_low)&(occ_and_elev["occupancy"]<=occupancy_set_high)]


with row4_2:
    st.write("")
    st.write(f"počet zobrazených stanic:    {str(len(data_kepler))} ")


#kepler_mapa
if occupancy_dif > 50:
  visual_channel = {'colorField': {'name': 'occupancy', 'type': 'real'},
      'colorScale': 'quantile',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear'}
else:
  visual_channel = {'colorField': None,
      'colorScale': 'quantile',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear'}

config = {'version': 'v1',
 'config': {'visState': {'filters': [],
   'layers': [{'id': 'idrvzkr',
     'type': 'point',
     'config': {'dataId': 'occupancy',
      'label': 'Point',
      'color': [0, 90, 50],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'lat': 'latitude', 'lng': 'longitude', 'altitude': None},
      'isVisible': True,
      'visConfig': {'radius': 14,
       'fixedRadius': False,
       'opacity': 0.96,
       'outline': False,
       'thickness': 2,
       'strokeColor': None,
       'colorRange': {'name': 'ColorBrewer YlGn-7',
        'type': 'sequential',
        'category': 'ColorBrewer',
        'colors': ['#ffffcc',
         '#d9f0a3',
         '#addd8e',
         '#78c679',
         '#41ab5d',
         '#238443',
         '#005a32']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radiusRange': [0, 50],
       'filled': True},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': visual_channel},
    {'id': 'cbp9hii',
     'type': 'point',
     'config': {'dataId': 'stations',
      'label': 'Point',
      'color': [137, 137, 137],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'lat': 'latitude', 'lng': 'longitude', 'altitude': None},
      'isVisible': False,
      'visConfig': {'radius': 10,
       'fixedRadius': False,
       'opacity': 0.45,
       'outline': False,
       'thickness': 2,
       'strokeColor': None,
       'colorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radiusRange': [0, 50],
       'filled': True},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': None,
      'colorScale': 'quantile',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear'}}],
   'interactionConfig': {'tooltip': {'fieldsToShow': {'occupancy': [{'name': 'occupancy',
        'format': None},
       {'name': 'place', 'format': None},
       {'name': 'elevation', 'format': None}],
      'stations': [{'name': 'occupancy', 'format': None},
       {'name': 'place', 'format': None},
       {'name': 'elevation', 'format': None}]},
     'compareMode': False,
     'compareType': 'absolute',
     'enabled': True},
    'brush': {'size': 0.5, 'enabled': False},
    'geocoder': {'enabled': False},
    'coordinate': {'enabled': False}},
   'layerBlending': 'normal',
   'splitMaps': [],
   'animationConfig': {'currentTime': None, 'speed': 1}},
  'mapState': {'bearing': 0,
   'dragRotate': False,
   'latitude': 49.19535222544416,
   'longitude': 16.593119848353272,
   'pitch': 0,
   'zoom': 12.8,
   'isSplit': False},
  'mapStyle': {'styleType': 'light',
   'topLayerGroups': {},
   'visibleLayerGroups': {'label': True,
    'road': True,
    'border': False,
    'building': True,
    'water': True,
    'land': True,
    '3d building': False},
   'threeDBuildingColor': [218.82023004728686,
    223.47597962276103,
    223.47597962276103],
   'mapStyles': {}}}}

map = KeplerGl(height=700, config=config)

map.add_data(data=data_kepler, name='occupancy')
map.add_data(data=official, name='stations')
keplergl_static(map, read_only = True)

