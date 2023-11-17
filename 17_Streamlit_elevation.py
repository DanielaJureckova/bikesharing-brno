import streamlit as st
import pandas as pd
import time 
import plotly.express as px
import matplotlib.pyplot as plt

import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl

import plotly.graph_objects as go




############
### DATA ###
############
st.set_page_config(
    page_title="Bikesharing Brno",
    page_icon="🚲",
    layout="wide",
)

palette = ['#024698', '#c54885', '#e32c83', '#bfa8cc', '#fbf9fc']

############
### DATA ###
############

#data_výpůjčky
data1 = pd.read_csv("data/23-11-16_20-25_address+places_id.csv")
addresses = pd.read_csv("data/address.csv")
places = pd.read_csv("data/places.csv")
stations = pd.read_csv("official_stations_rekola_nextbike.csv")

#data transformace
data = pd.merge(data1, places, left_on = "start_place_id", right_on = "place_id")
data.drop(columns=['place_id', "ID"], inplace = True)
data.rename(columns = {"place": "start_place"}, inplace=True)
data = pd.merge(data, places, left_on = "end_place_id", right_on = "place_id" )
data.drop(columns=['place_id', "ID"], inplace = True)
data.rename(columns = {"place": "end_place"}, inplace=True)
data["elevation_dif"] = data["elevation_dif"]*(-1)

    
#################
### SELECTION ###
#################
### COMPANY ###
st.sidebar.markdown("**Filtrování dat:** 👇")
companies = ["nextbike", "rekola"]
sel_company = st.sidebar.multiselect('Vyber společnost:', companies, companies)   #upravit barvičky?
data_company_filtered = data[data["company"].isin(sel_company)]

### YEAR ###
years = (data["year"].astype(int)).unique()
year = st.sidebar.multiselect('Vyber rok:', years, years)
data_company_year_filtered = data_company_filtered[data_company_filtered["year"].isin(year)]

### MONTH ###
months_czech = {
    4: "duben",
    5: "květen",
    6: "červen",
    7: "červenec",
    8: "srpen",
    9: "září",
    10: "říjen"
}
months = list(months_czech.values())
month = st.sidebar.multiselect('Vyber měsíc:', months, months)
filtered_data = data_company_year_filtered[data_company_year_filtered["month"].map(months_czech).isin(month)]


# english_to_czech_day_names = {
#     "Monday": "Pondělí",
#     "Tuesday": "Úterý",
#     "Wednesday": "Středa",
#     "Thursday": "Čtvrtek",
#     "Friday": "Pátek",
#     "Saturday": "Sobota",
#     "Sunday": "Neděle"
# }

# default_weekdays = list(english_to_czech_day_names.values())

# selected_weekdays = st.sidebar.multiselect("Vyber dny", default_weekdays, default_weekdays)

# filtered_data = data_com_y_m_filtered[data_com_y_m_filtered["start_time"].dt.day_name().map(english_to_czech_day_names).isin(selected_weekdays)]

# filtered_data = filtered_data[["name", "occupancy"]].groupby(by = "name").mean()
# occ_and_elev = filtered_data.merge(official, on ='name', how='inner')

# stations_full = occ_and_elev[occ_and_elev["occupancy"] > 0.98]["name"].reset_index(drop=True)
# stations_empty = occ_and_elev[occ_and_elev["occupancy"] < 0.05]["name"].reset_index(drop=True)

st.subheader("⛰️ Nadmořská výška")

st.markdown("---")



data_hist_up = filtered_data[filtered_data["elevation_dif"] > 0]
data_hist_up["dir"] = "up"
data_hist_down = filtered_data[filtered_data["elevation_dif"] < 0]
data_hist_down["dir"] = "down"
data_hist_down["elevation_dif"] = data_hist_down["elevation_dif"]*(-1)
data_hist = pd.concat([data_hist_up, data_hist_down])

threshold = 10
up = filtered_data[filtered_data["elevation_dif"] > threshold]
down = filtered_data[filtered_data["elevation_dif"] < (threshold*(-1))]
flat = filtered_data[(filtered_data["elevation_dif"] < threshold)&(filtered_data["elevation_dif"] > (threshold*(-1)))]

row1_spacer0, row1_1, row1_spacer1, row1_2, row1_spacer2   = st.columns((.2, 5, 1, 2, .2))
 
with row1_1:
    st.subheader('Četnost výpůjček vs. výškový rozdíl výpůjčky')    
    num_bins = 10

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data_hist_up["elevation_dif"],
        name='cesty  ↗️', # name used in legend and hover labels
        xbins=dict( # bins used for histogram
            start=0,
            end=50,
            size=num_bins
        ),
        marker_color='#B8D4FF',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=data_hist_down["elevation_dif"],
        name='cesty  ↘️',
        xbins=dict(
            start= 0,
            end= 50,
            size=num_bins
        ),
        marker_color='#32527B',
        opacity=0.75
    ))
    fig.update_xaxes(dtick= 10) 
    fig.update_layout(width = 600,
        xaxis_title_text='změna nadmořské výšky během výpůjčky', 
        yaxis_title_text='četnost',
        bargap=0.1, # gap between bars of adjacent location coordinates
        bargroupgap= 0.0, # gap between bars of the same location coordinates
        legend=dict(
        yanchor="top",
        y=1,
        xanchor= "right",
        x=1, font=dict(size=16)),
        margin = dict(t=10) 
    )

    st.plotly_chart(fig, use_container_width = True)


with row1_2:
    st.metric(label = "Výpůjčky po rovině (+- 10 m)", value = str('{:,.0f}'.format(len(flat)).replace(',', ' ')))
    st.metric(label = "Výpůjčky   ↗️", value = str('{:,.0f}'.format(len(up)).replace(',', ' ')))
    st.metric(label = "Výpůjčky   ↘️", value = str('{:,.0f}'.format(len(down)).replace(',', ' ')))
    st.metric(label = "Nastoupáno", value = f"{str('{:,.0f}'.format(up['elevation_dif'].sum()).replace(',', ' '))} m")
    st.metric(label = "Naklesáno", value = f"{str('{:,.0f}'.format(abs(down['elevation_dif'].sum())).replace(',', ' '))} m")


st.markdown("---")

row2_spacer0, row2_1,  = st.columns((.2, 10 ))
st.subheader("Výpůjčky s největším rozdílem nadmořských výšek a nejvýše položené stanice")

top_up_trips = filtered_data[["start_place", "end_place", "elevation_dif"]].groupby(["start_place","end_place", "elevation_dif"]).size().reset_index(name='count')
top_up_trips_sorted = top_up_trips.nlargest(50, 'elevation_dif').reset_index()
tops = top_up_trips_sorted.merge(stations, left_on = "start_place", right_on = "place", right_index = False)
tops.rename(columns = {"latitude":"start_latitude", "longitude":"start_longitude"}, inplace = True)
tops = tops.drop(["elevation", "nextbike", "rekola", "place"], axis = 1)
tops2 = tops.merge(stations, left_on = "end_place", right_on = "place", right_index = False)
tops2.rename(columns = {"latitude":"end_latitude", "longitude":"end_longitude"}, inplace = True)
tops2 = tops2.drop(["elevation", "nextbike", "rekola", "place"], axis = 1)
highest_points = tops2.drop_duplicates("end_place")


config = {'version': 'v1',
 'config': {'visState': {'filters': [],
   'layers': [{'id': '9b2xjx',
     'type': 'arc',
     'config': {'dataId': 'data1',
      'label': 'start -> end line',
      'color': [183, 136, 94],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'lat0': 'start_latitude',
       'lng0': 'start_longitude',
       'lat1': 'end_latitude',
       'lng1': 'end_longitude'},
      'isVisible': True,
      'visConfig': {'opacity': 0.8,
       'thickness': 2,
       'colorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#FFC300',
         '#F1920E',
         '#E3611C',
         '#C70039',
         '#900C3F',
         '#5A1846'],
        'reversed': True},
       'sizeRange': [0, 10],
       'targetColor': None},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': 'elevation_dif',
       'type': 'integer'},
      'colorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear'}},
    {'id': '96jokp4',
     'type': 'point',
     'config': {'dataId': 'tops',
      'label': 'tops',
      'color': [246, 209, 138],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'lat': 'end_latitude',
       'lng': 'end_longitude',
       'altitude': None},
      'isVisible': True,
      'visConfig': {'radius': 10,
       'fixedRadius': False,
       'opacity': 0.8,
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
      'textLabel': [{'field': {'name': 'end_place', 'type': 'string'},
        'color': [214, 214, 213],
        'size': 15,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': None,
      'colorScale': 'quantile',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear'}}],
   'interactionConfig': {'tooltip': {'fieldsToShow': {'data1': [{'name': 'start_place',
        'format': None},
       {'name': 'end_place', 'format': None},
       {'name': 'elevation_dif', 'format': None}],
      'tops': [{'name': 'index', 'format': None},
       {'name': 'start_place', 'format': None},
       {'name': 'end_place', 'format': None},
       {'name': 'elevation_dif', 'format': None},
       {'name': 'count', 'format': None}]},
     'compareMode': False,
     'compareType': 'absolute',
     'enabled': True},
    'brush': {'size': 0.5, 'enabled': False},
    'geocoder': {'enabled': False},
    'coordinate': {'enabled': False}},
   'layerBlending': 'normal',
   'splitMaps': [],
   'animationConfig': {'currentTime': None, 'speed': 1}},
  'mapState': {'bearing': 24,
   'dragRotate': True,
   'latitude': 49.211561998562146,
   'longitude': 16.594472188780358,
   'pitch': 50,
   'zoom': 11.349228408499641,
   'isSplit': False},
  'mapStyle': {'styleType': 'dark',
   'topLayerGroups': {},
   'visibleLayerGroups': {'label': True,
    'road': True,
    'border': False,
    'building': True,
    'water': True,
    'land': True,
    '3d building': False},
   'threeDBuildingColor': [9.665468314072013,
    17.18305478057247,
    31.1442867897876],
   'mapStyles': {}}}}
     
map = KeplerGl(height=500, config=config)

map.add_data(data=tops2, name='data1',)
map.add_data(data=highest_points, name='tops')
keplergl_static(map, read_only = True)
