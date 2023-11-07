import streamlit as st
import pandas as pd
import time 
import plotly.express as px
import matplotlib.pyplot as plt

import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium


def occup_zero_one(row):
    if row['bikes'] > 1:
        # Do something with the row when the condition is met
        return 1
    else:
        # Do something else when the condition is not met
        return row['bikes'] 

stations = pd.read_csv("data.csv")
stations = stations[stations["bike"] == False]
stations["date-time"] = stations["date"] + " " + stations["time"] 
stations["date-time"] = pd.to_datetime(stations["date-time"], format="%d/%m/%Y %H:%M:%S", errors = "coerce")
official = pd.read_csv("23-11-05_nxtb_stations_scrap.csv")

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="🚲",
    layout="wide",
)


st.title("🚲🚲Oficiální nextbike stanice🚲🚲")

st.sidebar.header("Time Filter Options")


# Create sliders to select the start and end hours
hour_range = st.sidebar.slider("Select Hour Range", 0, 23, (0, 23))

start_hour, end_hour = hour_range

default_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
selected_weekdays = st.sidebar.multiselect("Select Weekdays", default_weekdays, default_weekdays)

# Filter stations based on selected hours
filtered_data = stations[
    (stations["date-time"].dt.hour >= start_hour) & (stations["date-time"].dt.hour <= end_hour) &
    (stations["date-time"].dt.day_name().isin(selected_weekdays))
]

filtered_data["occupancy"] = filtered_data.apply(occup_zero_one, axis=1)

filtered_data = filtered_data[["name", "occupancy"]].groupby(by = "name").mean()
occ_and_elev = filtered_data.merge(official, on ='name', how='inner')

stations_full = occ_and_elev[occ_and_elev["occupancy"] > 0.98]["name"].reset_index(drop=True)
stations_empty = occ_and_elev[occ_and_elev["occupancy"] < 0.05]["name"].reset_index(drop=True)

fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    brno_location = Nominatim(user_agent="brno_location").geocode("Brno, Czech Republic")
    brno_map = folium.Map(location=[brno_location.latitude, brno_location.longitude], zoom_start=13)

    def color_picker(value):
        if value < 0.25:
            return 'grey'
        elif value < 0.5:
            return 'red'
        elif value < 0.75:
            return 'orange'
        else:
            return 'green'

    for index, row in occ_and_elev.iterrows():
        tooltip = row[['name', 'occupancy']]
        folium.CircleMarker(
            location=[row['lat'], row['lng']],
            radius=3,
            color=color_picker(row['occupancy']),
            fill=True,
            fill_color=color_picker(row['occupancy']),
            fill_opacity=1,
            popup=f"Value: {row['occupancy']}", tooltip = tooltip).add_to(brno_map)

    st.markdown("### mapa")
    #pokus 
    make_map_responsive= """
    <style>
    [title~="st.iframe"] { width: 100%}
    </style>
    """
    st.markdown(make_map_responsive, unsafe_allow_html=True)
    st_data = st_folium(brno_map)




with fig_col2:
    st.markdown("### plné stanice (obsazenost > 98%)")
    for a in stations_full:
        st.write(a)
 

