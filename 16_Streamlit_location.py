import streamlit as st
import pandas as pd

import plotly.express as px
import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl

##########################
### PAGE CONFIGURATION ###
##########################
st.set_page_config(
    page_title="Bikesharing Brno",
    page_icon="🚲",
    layout="wide")


############
### DATA ###
############
data = pd.read_csv("data/23-11-11_20-00_data_all_offstations.csv")
stations_nextbike = pd.read_csv("official_nextbike_stations.csv")
stations_rekola = pd.read_csv("official_rekola_stations.csv")
stations_nextbike["company"] = "nextbike"
stations_rekola["company"] = "rekola"

#dataset_with start_end location separated
dataset_start = data[['start_time', 'user_id', 'start_latitude',
       'start_longitude', 'company', 'start_location', 'start_address',
        'start_street', 'start_elevation', "start_place"]]
dataset_start["start_end"] = "start"
dataset_start = dataset_start.rename(columns = {'start_time':'time', 'start_latitude':'latitude',
       'start_longitude': 'longitude', 'start_location':'location', 'start_address':'address',
        'start_street':'street', "start_place":"place", 'start_elevation':'elevation'})

dataset_end = data[['end_time', 'user_id', 'end_latitude',
       'end_longitude', 'company', 'end_location', 'end_address',
        'end_street', 'end_elevation', "end_place"]]
dataset_end["start_end"] = "end"
dataset_end = dataset_end.rename(columns = {'end_time':'time', 'end_latitude':'latitude',
       'end_longitude': 'longitude', 'end_location':'location', 'end_address':'address',
        'end_street':'street', "end_place": "place", 'end_elevation':'elevation'})
dataset_start_end = pd.concat([dataset_start, dataset_end])

nxt_par = False
rek_par = False

#################
### FUNCTIONS ###
#################

def create_heatmap(kepler_data, nxt_par, rek_par):    
    config = {'version': 'v1',
    'config': {'visState': {'filters': [],
    'layers': [{'id': '3fbk3hd',
        'type': 'heatmap',
        'config': {'dataId': 'all_data',
        'label': 'heatmap',
        'color': [136, 87, 44],
        'highlightColor': [252, 242, 26, 255],
        'columns': {'lat': 'latitude', 'lng': 'longitude'},
        'isVisible': True,
        'visConfig': {'opacity': 0.8,
        'colorRange': {'name': 'Global Warming',
            'type': 'sequential',
            'category': 'Uber',
            'colors': ['#5A1846',
            '#900C3F',
            '#C70039',
            '#E3611C',
            '#F1920E',
            '#FFC300']},
        'radius': 55.7},
        'hidden': False,
        'textLabel': [{'field': None,
            'color': [255, 255, 255],
            'size': 18,
            'offset': [0, 0],
            'anchor': 'start',
            'alignment': 'center'}]},
        'visualChannels': {'weightField': {'name': 'hustota výpůjček',
        'type': 'real'},
        'weightScale': 'linear'}},
        {'id': 'ulpp2dk',
        'type': 'point',
        'config': {'dataId': 'rekola',
        'label': 'rekola',
        'color': [218, 112, 191],
        'highlightColor': [252, 242, 26, 255],
        'columns': {'lat': 'latitude', 'lng': 'longitude', 'altitude': None},
        'isVisible': rek_par,
        'visConfig': {'radius': 8,
        'fixedRadius': False,
        'opacity': 0.25,
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
        'sizeScale': 'linear'}},
        {'id': 'jyed6bj',
        'type': 'point',
        'config': {'dataId': 'nextbike',
        'label': 'nextbike',
        'color': [59, 133, 204],
        'highlightColor': [252, 242, 26, 255],
        'columns': {'lat': 'latitude', 'lng': 'longitude', 'altitude': None},
        'isVisible': nxt_par,
        'visConfig': {'radius': 8,
        'fixedRadius': False,
        'opacity': 0.25,
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
        'sizeScale': 'linear'}},
        {'id': 'aytb9p9',
        'type': 'point',
        'config': {'dataId': 'all_data',
        'label': 'locations',
        'color': [231, 159, 213],
        'highlightColor': [252, 242, 26, 255],
        'columns': {'lat': 'latitude', 'lng': 'longitude', 'altitude': None},
        'isVisible': True,
        'visConfig': {'radius': 10,
        'fixedRadius': False,
        'opacity': 0,
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
    'interactionConfig': {'tooltip': {'fieldsToShow': {'all_data': [{'name': 'address',
            'format': None}],
        'rekola': [{'name': 'place', 'format': None}],
        'nextbike': [{'name': 'place', 'format': None}]},
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
    'latitude': 49.198073396065475,
    'longitude': 16.606715650106903,
    'pitch': 0,
    'zoom': 13.258770704349452,
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

    keplermap = KeplerGl(height=700, config = config)
    keplermap.add_data(data = kepler_data, name='all_data')

    #vyhodit někam ven
    nextbike_stations = pd.read_csv("official_nextbike_stations.csv")
    rekola_stations = pd.read_csv("official_rekola_stations.csv")

    keplermap.add_data(data = rekola_stations, name='rekola')

    keplermap.add_data(data = nextbike_stations, name='nextbike')

    return keplermap

#################
### FILTERING ###
#################

### COMPANY ###
st.sidebar.markdown("**Filtrování dat:** 👇")
companies = ["nextbike", "rekola"]
sel_company = st.sidebar.multiselect('Vyber společnost:', companies, companies)   #upravit barvičky?
data_company_filtered = dataset_start_end[dataset_start_end["company"].isin(sel_company)]

### YEAR ###
data_company_filtered["year"] = (pd.to_datetime(data_company_filtered["time"])).dt.year
years = data_company_filtered["year"].unique()
year = st.sidebar.multiselect('Vyber rok:', years, years)
data_company_year_filtered = data_company_filtered[data_company_filtered["year"].isin(year)]

### MONTH ###
data_company_year_filtered["month"] = (pd.to_datetime(data_company_year_filtered["time"])).dt.month
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
top_location = data_all_filtered.value_counts("street").nlargest(3) 

row0_spacer1, row1_1, row1_spacer2 = st.columns((.2, 7.1, .2))
with row1_1:
    st.subheader("📍 Nejpopulárnější lokality:")

st.markdown("---")

row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3,   = st.columns((.2, 2, .2, 5.2, .2))
with row2_1:
    str_rentals = f"Nejvytíženější lokality (ulice):" 
    st.markdown(str_rentals)    

with row2_2:
    st.markdown(f"🥇 {top_location.index[0]}")  
    st.markdown(f"🥈 {top_location.index[1]}" )
    st.markdown(f"🥉 {top_location.index[2]}" )

st.markdown("---")

################
### HEATMAPA ###
################
###data for heatmap
data_all_filtered["latitude"] = data_all_filtered["latitude"].round(5)
data_all_filtered["longitude"] = data_all_filtered["longitude"].round(5)

map_data_start = data_all_filtered[["address","latitude", "longitude"]].groupby(["address"]).agg({'latitude': 'median', 'longitude': 'median'}).reset_index()
address_counts = data_all_filtered['address'].value_counts().reset_index()
address_counts.columns = ['address', 'count']
map_data_start = pd.merge(map_data_start, address_counts, on='address')
map_data_start = map_data_start.sort_values(by="count")
map_data_start["hustota výpůjček"] = map_data_start["count"]/(map_data_start["count"].max()/10) 

row3_spacer0, row_3_0, row3_spacer1, row_3_1, row3_spacer2 = st.columns((.2, 5.5, .2, 1.5, .2))

with row_3_1:
    st.write(" ")
    st.write(" ")
    st.write(" ")
    stations_to_show = st.selectbox("Zobraz oficiální stanice", ["nezobrazuj", "nextbike", "rekola", "nextbike + rekola"], index=0)
    if stations_to_show == "nextbike":
         nxt_par = True
    elif stations_to_show == "rekola":
         rek_par = True
    elif stations_to_show == "nextbike + rekola":
         rek_par = True
         nxt_par = True

with row_3_0: 
     
    keplergl_static(create_heatmap(map_data_start, nxt_par, rek_par))


st.markdown("---")

row4_spacer0, row4_1 = st.columns((.2, 4))
with row4_1:
    st.subheader("Oficiální stanice: hodnocení podle počtu výpůjček:")
   

row5_spacer0, row5_1, row5_spacer1, row5_2, row5_spacer2 = st.columns((.2, 2, .2, 7, .2))

with row5_1:
    start_end_dict = {
        "start": "začátek výpůjčky",
        "end": "konec výpůjčky",
    }

    start_end = st.selectbox("Půjčování vs. vracení:", ["začátek výpůjčky", "konec výpůjčky", "vše"], index=0)
    if start_end == "vše":
        data_start_end_fil = data_all_filtered
    else:
        data_start_end_fil = data_all_filtered[data_all_filtered["start_end"].map(start_end_dict) == start_end]


row6_spacer0, row6_1, row6_spacer1 = st.columns((.2, 6, .2))

with row6_1:
    top_stations = data_start_end_fil.value_counts("place").nlargest(10).index.tolist() 
    top10 = data_start_end_fil[data_start_end_fil["place"].isin(top_stations)]
    st.write("Nejvytíženější stanice:")
    bar_top = px.bar(top10, 
                     y = "place", 
                     orientation='h', 
                     color= "company", 
                     hover_data = {"place":False, "company":False},
                     color_discrete_map = {"rekola":'deeppink', "nextbike":"navy"}, 
                     category_orders={"place": top10.value_counts("place").index})
    bar_top.update_layout(
        xaxis_title = "",
        yaxis_title = "", 
        margin=dict(l=0, r=0, t=3, b=0),
        legend_title = None,
        showlegend = False,
        width = 600
        )
    bar_top.update_traces(hovertemplate=None,
    hoverinfo='skip')

    st.plotly_chart(bar_top )




        