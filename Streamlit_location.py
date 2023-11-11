import streamlit as st
import pandas as pd
import time 
import plotly.express as px
import matplotlib.pyplot as plt

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

from geopy.geocoders import Nominatim

##########################
### PAGE CONFIGURATION ###
##########################
st.set_page_config(
    page_title="Bikesharing Brno",
    page_icon="🚲",
    layout="wide",
)


# def filter_company(df_data):
#     data_company_filtred = pd.DataFrame()
#     if all_teams_selected == 'Select teams manually (choose below)':
#         df_filtered_team = df_data[df_data['team'].isin(selected_teams)]
#         return df_filtered_team
#     return data



palette = ['#024698', '#c54885', '#e32c83', '#bfa8cc', '#fbf9fc']

############
### DATA ###
############
data = pd.read_csv("23-10-31_data_filtered_weather_elevation.csv")
stations_nextbike = pd.read_csv("official_nextbike_stations.csv")
stations_rekola = pd.read_csv("official_rekola_stations.csv")
stations_nextbike["company"] = "nextbike"
stations_rekola["company"] = "rekola"
stations = pd.concat([stations_nextbike, stations_rekola], axis = 0).reset_index(drop=True)


#################
### FILTERING ###
#################

### COMPANY ###
st.sidebar.markdown("**Filtrování dat:** 👇")
companies = ["nextbike", "rekola"]
sel_company = st.sidebar.multiselect('Vyber společnost:', companies, companies)   #upravit barvičky?
data_company_filtered = data[data["company"].isin(sel_company)]

### Year ###
data ["year"] = (pd.to_datetime(data["start_time"])).dt.year
years = data ["year"].unique()
year = st.sidebar.multiselect('Vyber rok:', years, years)
data_company_year_filtered = data_company_filtered[data_company_filtered["year"].isin(year)]

### Month ###
data["month"] = (pd.to_datetime(data["start_time"])).dt.month
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
data_all_filtered = data_company_year_filtered[data_company_year_filtered["month"].map(months_czech).isin(month)]


################
### SEE DATA ###
################
row0_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader("Nejpopulárnější lokality:")

 
top_location = pd.concat([data_all_filtered["start_street"], data_all_filtered["end_street"]], ignore_index = True).value_counts("street").nlargest(3) 

row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4, row2_4    = st.columns((.2, 1.8, .2, 1.2, .2, 1.2, .2, 3 ))
with row2_1:
    str_rentals = f"Pro  {str(len(data_all_filtered))} vybraných výpůjček 🚲 :" 
    st.markdown(str_rentals)    

with row2_2:
    st.markdown(f" 🥇 {top_location.index[0]}")  

with row2_3:
    st.markdown(f"🥈 {top_location.index[1]}" )

with row2_4:
    st.markdown(f"🥉 {top_location.index[2]}" )

################
### HEATMAPA ###
################


data_all_filtered["start_latitude"] = data_all_filtered["start_latitude"].round(5)
data_all_filtered["start_longitude"] = data_all_filtered["start_longitude"].round(5)

map_data_start = data_all_filtered[["start_address","start_latitude", "start_longitude"]].groupby(["start_address"]).agg({'start_latitude': 'median', 'start_longitude': 'median'}).reset_index()
address_counts = data_all_filtered['start_address'].value_counts().reset_index()
address_counts.columns = ['start_address', 'count']
map_data_start = pd.merge(map_data_start, address_counts, on='start_address')
map_data_start = map_data_start.sort_values(by="count")
map_data_start["hustota výpůjček"] = map_data_start["count"]/(map_data_start["count"].max()/10) 


import streamlit as st
import pandas as pd
import plotly.express as px
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.write("Mapa nejvytíženějších lokalit:")
fig = px.density_mapbox(
    map_data_start,
    lat='start_latitude',
    lon='start_longitude',
    z = 'hustota výpůjček',
    radius=23, 
    center=dict(lat=data_all_filtered['start_latitude'].mean(), lon=data_all_filtered['start_longitude'].mean()),
    zoom=12.5,
    range_color=[-0.2, 1.1],
    mapbox_style = "open-street-map",  #open-street-map": Standardní OpenStreetMap dlaždicová mapa, "carto-positron" a "carto-darkmatter"
    opacity = 0.6,
    height = 600,
    width = 900,
    hover_name = 'start_address',
    hover_data={'start_address': False, 'start_latitude': False, "start_longitude": False, "count": False,"hustota výpůjček":False },
    labels={'start_address': 'start_address'},
    color_continuous_scale='Reds') #Reds #thermal

fig.update_coloraxes(showscale=False)
fig.update_layout( margin=dict(l=20, r=20, t=5, b=5),
)


if len(sel_company) == 2:
    fig.add_trace(px.scatter_mapbox(
        stations_nextbike,
        lat='latitude',
        lon='longitude',
        color = "company",
        opacity = 0.75,
        size_max = 0.5,
        hover_data={'latitude':False, 'longitude':False, 'company':False},
        color_discrete_sequence=['#024698']
    ).data[0])

    fig.add_trace(px.scatter_mapbox(
        stations_rekola,
        lat = 'latitude',
        lon = 'longitude',
        hover_data={'latitude':False, 'longitude':False, 'company':False},
        color = 'company',
        opacity = 0.6,
        size_max = 0.5,
        color_discrete_sequence=['#c54885']
    ).data[0])

elif sel_company[0] == "nextbike":
     fig.add_trace(px.scatter_mapbox(
        stations,
        lat='latitude',
        lon='longitude',
        hover_data={'latitude':False, 'longitude':False,  'company':False},
        color = 'company',
        opacity = 0.8,
        size_max = 0.5,
        color_discrete_sequence=['#024698', '#c54885']
    ).data[0])

elif sel_company[0] == "rekola":
     fig.add_trace(px.scatter_mapbox(
        stations_rekola,
        lat='latitude',
        lon='longitude',
        hover_data={'latitude':False, 'longitude':False, 'company':False},
        color = "company",
        opacity = 0.8,
        size_max = 0.5,
        color_discrete_sequence=['#c54885']
    ).data[0])
     
elif len(sel_company) == 0:
    pass

fig.update_layout(showlegend=False) 


# Zobrazte heatmapu pomocí Streamlit
st.plotly_chart(fig)






