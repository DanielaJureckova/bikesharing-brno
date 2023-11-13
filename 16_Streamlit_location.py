import streamlit as st
import pandas as pd

import plotly.express as px

##########################
### PAGE CONFIGURATION ###
##########################
st.set_page_config(
    page_title="Bikesharing Brno",
    page_icon="🚲",
    layout="wide",
)

palette = ['#024698', '#c54885', '#e32c83', '#bfa8cc', '#fbf9fc']

############
### DATA ###
############
data = pd.read_csv("data/23-11-11_20-00_data_all_offstations.csv")
stations_nextbike = pd.read_csv("official_nextbike_stations.csv")
stations_rekola = pd.read_csv("official_rekola_stations.csv")
stations_nextbike["company"] = "nextbike"
stations_rekola["company"] = "rekola"
stations = pd.concat([stations_nextbike, stations_rekola], axis = 0).reset_index(drop=True)


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

def create_heatmap(data, n_par, r_par):
        import plotly.express as px
        st.write("Mapa nejvytíženějších lokalit:")
        fig = px.density_mapbox(
            map_data_start,
            lat='latitude',
            lon='longitude',
            z = 'hustota výpůjček',
            radius=55, 
            center=dict(lat=49.19374, lon=16.60545),
            zoom=14,
            range_color=[-0.1, 0.5],
            mapbox_style = "carto-darkmatter",  #open-street-map": Standardní OpenStreetMap dlaždicová mapa, "carto-positron" a "carto-darkmatter"
            opacity = 0.6,
            height = 600,
            width = 850,
            hover_name = 'address',
            hover_data={'address': False, 'latitude': False, "longitude": False, "count": False,"hustota výpůjček":False },
            labels={'address': 'address'},
            color_continuous_scale='inferno') #Reds #thermal
        
        if nxt_par == True:
            fig.add_trace(px.scatter_mapbox(
                stations_nextbike,
                lat='latitude',
                lon='longitude',
                color = "company",
                opacity = 0.5,
                size_max = 0.25,
                hover_name = "place",
                hover_data={"place": False,'latitude':False, 'longitude':False, 'company':False},
                color_discrete_sequence=['#89CFF0']
            ).data[0])

        if rek_par == True:
            fig.add_trace(px.scatter_mapbox(
                stations_rekola,
                lat='latitude',
                lon='longitude',
                color = "company",
                opacity = 0.5,
                size_max = 0.25,
                hover_name = "place",
                hover_data={"place": False, 'latitude':False, 'longitude':False, 'company':False},
                color_discrete_sequence=['#ffb6c1']
            ).data[0])

        fig.update_coloraxes(showscale=False)
        fig.update_layout( margin=dict(l=0, r=0, t=3, b=0))
        fig.update_layout(showlegend=False) 

        return fig

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

row0_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
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
    
         
    #plot map
    st.plotly_chart(create_heatmap(map_data_start, nxt_par, rek_par))


st.markdown("---")

row4_spacer0, row4_1, row4_spacer2, row4_2, row4_spacer3 = st.columns((.2, 4, .2, 8 ,0.2))
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


row6_spacer0, row6_1, row6_spacer1, row6_2, row6_spacer2 = st.columns((.2, 4, .2, 3, .2))

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

with row6_2:
    low_stations = data_start_end_fil.value_counts("place").nsmallest(10).index.tolist() 
    low10 = data_start_end_fil[data_start_end_fil["place"].isin(low_stations)]
    st.write("Nejopuštěnější stanice:")
    bar_low = px.bar(low10, 
                     y = "place", 
                     orientation='h', 
                     color= "company", 
                     hover_data = {"place":False, "company":False},
                     color_discrete_map = {"rekola":'deeppink', "nextbike":"navy"}, 
                     category_orders={"place": low10.value_counts("place").sort_values(ascending=True).index})
    bar_low.update_layout(
        xaxis_title = "",
        yaxis_title = "", 
        margin=dict(l=0, r=0, t=3, b=0),
        legend_title = None,
        width = 500,
        )
    bar_low.update_traces(hovertemplate=None,
    hoverinfo='skip')

    st.plotly_chart(bar_low )

st.write("????přidat komentář, že nemusí být směrodatné, poněvadž v určitých lokalitách jsou mohou být stanice blízko sebe a tak dojde k rozpadu??") 
st.write("note: masterpiece by byl mít nějaký tooltip, který by následně zvýrazil bod do mapy, ale tam teda ještě nejsem :)") 




        