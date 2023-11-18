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
data = pd.read_csv("data/23-11-18_occ_and_elevation_nextbike.csv")


#page
st.subheader("Obsazenost stanic společnosti Nextbike")

st.write("Průměrné hodnoty obsazenosti stanic společnosti Nextbike v období 21.9.2023 - 09.11.2023.")
st.markdown("---")


col2_spacer0, col2_1, col2_spacer1, col2_2, col2_spacer2, col2_3, col2_spacer3   = st.columns((1, 1.5, 0.2, 0.5, .2, 2, .2))

occ_90more = data[data['occupancy']>0.9]
occ_20less = data[data['occupancy']<0.2]
occ_50more = data[data['occupancy']>0.5]

with col2_1:
    st.write("📍")
    st.write("Celkový počet stanic")
    st.write("Stanice s obsazeností > 90%")
    st.write("Stanice s obsazeností > 50%")
    st.write("Stanice s obsazeností < 20%")

with col2_2:
    st.write("počet")
    st.write(str(len(data)))
    st.write(str(len(occ_90more)))
    st.write(str(len(occ_50more)))
    st.write(str(len(occ_20less)))

with col2_3:
    st.write("průměrná nadmořská výška")
    st.write(str(int(data['elevation'].mean())) + " m.n.m.")
    st.write(str(int(occ_90more['elevation'].mean())) + " m.n.m.")
    st.write(str(int(occ_50more['elevation'].mean()))+ " m.n.m.")
    st.write(str(int(occ_20less['elevation'].mean()))+ " m.n.m.")

st.markdown("---")

row3_spacer0, row3_1, row3_spacer1, row3_2, row3_spacer2   = st.columns((.2, 3, 1, 3, 0.2))
with row3_1:
    occupancy_set = st.slider("Rozsah obsazenosti(%):", 0, 100, (0,100),)
occupancy_set_low = occupancy_set[0]/100
occupancy_set_high = occupancy_set[1]/100 

data_kepler = data[(data["occupancy"]>=occupancy_set_low)&(data["occupancy"]<=occupancy_set_high)]


with row3_2:
    st.write("")
    st.write(f"počet zobrazených stanic:    {str(len(data_kepler))} ")


#kepler_mapa

config = {'version': 'v1',
 'config': {'visState': {'filters': [],
   'layers': [{'id': 'idrvzkr',
     'type': 'point',
     'config': {'dataId': 'occupancy',
      'label': 'Point',
      'color': [255, 153, 31],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'lat': 'latitude', 'lng': 'longitude', 'altitude': None},
      'isVisible': True,
      'visConfig': {'radius': 10,
       'fixedRadius': False,
       'opacity': 0.96,
       'outline': False,
       'thickness': 2,
       'strokeColor': None,
       'colorRange': {'name': 'ColorBrewer RdYlGn-6',
        'type': 'diverging',
        'category': 'ColorBrewer',
        'colors': ['#d73027',
         '#fc8d59',
         '#fee08b',
         '#d9ef8b',
         '#91cf60',
         '#1a9850']},
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
     'visualChannels': {'colorField': {'name': 'occupancy', 'type': 'real'},
      'colorScale': 'quantile',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear'}},
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
   'latitude': 49.19743627687811,
   'longitude': 16.591216589372696,
   'pitch': 0,
   'zoom': 11.850855130832366,
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
map.add_data(data=data, name='stations')
keplergl_static(map, read_only = True)
