import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bikesharing Brno", page_icon="🚲", layout="wide")
palette = ['#024698', '#c54885', '#e32c83', '#bfa8cc', '#fbf9fc']

st.title('Sdílená kola v Brně')
st.markdown('---')

# def rozdel_teplotu(teplota):
#     if teplota <= 5:
#         return '< 5'
#     elif teplota > 5 and teplota <= 10:
#         return '5-10'
#     elif teplota > 10 and teplota <= 15:
#         return '10-15'
#     elif teplota > 15 and teplota <= 20:
#         return '15-20'
#     elif teplota > 20 and teplota <= 25:
#         return '20-25'
#     elif teplota > 25 and teplota <= 30:
#         return '25-30'
#     elif teplota > 30 :
#         return '30+'

def rozdel_uhrn(rain):
    if rain == 0:
        return "sucho"
    elif rain <= 1:
        return 'mírný déšť (do 1 mm)'
    elif rain >  1:
        return 'silnější déšť (1 mm a více)'


def load_data():
    df = pd.read_csv("data/23-11-18_15-30_adresses_places_id.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    df = df[~((df['start_time'].dt.month == 4) & (df['start_time'].dt.day >= 1) & (df['start_time'].dt.day <= 10))]

    return df

df_dataset = load_data()
df_dataset["start_time"] = pd.to_datetime(df_dataset["start_time"], format="%Y-%m-%d %H:%M:%S")

df_weather = pd.read_csv('data/weather-22-to-05-11-23.csv')
df_weather["time"] = pd.to_datetime(df_weather["time"], format="%Y-%m-%dT%H:%M")

# data segmentation & resampling

dataset_for_merge = df_dataset.set_index('start_time')
dataset_for_merge['rental_number'] = 1
rentals_in_hours = dataset_for_merge['rental_number'].resample('H').sum()
merged_data = pd.merge(rentals_in_hours, df_weather, how = "left", left_on = "start_time", right_on = "time" )
merged_data["round_temperature"] = merged_data["temperature_2m (°C)"].round().astype(int)


#filtering
st.sidebar.header("👇 Filtrovací panel")

# year
years = df_dataset["year"].unique()
selected_years = st.sidebar.multiselect('Vyber rok', years,years)

df_dataset['is_day'] = df_dataset['is_day ()'].astype(bool)

filtered_data = df_dataset[df_dataset["year"].isin(selected_years)]
filtered_merged_data = merged_data[merged_data["time"].dt.year.isin(selected_years)]

#date
start_date = filtered_data['start_time'].min()
end_date = filtered_data['end_time'].max()
start_date_formatted = pd.to_datetime(start_date).strftime('%d.%m.%Y')
end_date_formatted = pd.to_datetime(end_date).strftime('%d.%m.%Y')

#metrics
max_temp = filtered_data['temperature_2m (°C)'].max()
min_temp = filtered_data['temperature_2m (°C)'].min()
avg_wind_speed = filtered_data['wind_speed_10m (km/h)'].mean()
max_wind_gust = filtered_data['wind_gusts_10m (km/h)'].max()
average_day_temp = filtered_data[filtered_data['is_day ()'] == 1]['temperature_2m (°C)'].mean()


front_spacer, text, table_column_1, table_column_2, table_column_3, back_spacer = st.columns((1.5, 1.5, 1.5, 0.5, 1.5, 1))
with front_spacer:
    st.subheader(f"Počasí za období: ") 
with text:
    st.markdown("")
    st.write(f"{start_date_formatted} - {end_date_formatted}")

with table_column_1:
    st.markdown("")
    st.markdown("🥵 Nejvyšší teplota")
    st.markdown("🥶 Nejnižší teplota")
    st.markdown("🌡️ Průměrná denní teplota")
    st.markdown("💨 Průměrná rychlost větru")
    st.markdown("💨 Největší náraz větru")

with table_column_2:
    st.markdown("")
    st.markdown(str(f"{max_temp} °C"))
    st.markdown(str(f"{min_temp} °C"))
    st.markdown(str(f"{average_day_temp:.1f} °C"))
    st.markdown(str(f"{avg_wind_speed:.1f} km/h"))
    st.markdown(str(f"{max_wind_gust:.1f} km/h"))
    
st.markdown("---")


#temperature
st.subheader("🌡️ Teplotní analýza")

#
temperature_slider = st.sidebar.slider("Vyber rozsah teploty", min_value=min_temp, max_value=max_temp, value=(min_temp,max_temp))

filtered_data = filtered_data[(filtered_data['round_temperature'] >= temperature_slider[0]) & (filtered_data['round_temperature'] <= temperature_slider[1])]
filtered_merged_data = filtered_merged_data[(filtered_merged_data['round_temperature'] >= temperature_slider[0]) & (filtered_merged_data['round_temperature'] <= temperature_slider[1])]

filter_column, middle_spacer, fig_column, back_spacer = st.columns((0.5, 0.2, 0.5, 1))

with filter_column:
    graph_options = st.selectbox("Vyber metriku", ("Průměrná délka jízdy", "Počet jízd - celkem","Počet jízd - hodinový průměr", "Počet uživatelů - celkem","Najetý čas - celkem"))
    filtered = ''

    if graph_options == "Průměrná délka jízdy":
        rental_length = filtered_data[~((filtered_data["duration_min"]>100)&(filtered_data["round_temperature"] == 0))]
        y_axis = 'average_ride_length'
        filtered =['round_temperature']
        df_graph = rental_length.groupby(filtered)['duration_min'].mean().reset_index(name=y_axis)
    elif graph_options == "Počet jízd - celkem":
        y_axis = 'rides_number'
        filtered=['round_temperature']
        df_graph = filtered_data.groupby(filtered).size().reset_index(name=y_axis)
    elif graph_options == "Počet uživatelů - celkem":
        y_axis = 'total_users'
        filtered=['round_temperature']
        df_graph = filtered_data.groupby(filtered)['user_id'].nunique().reset_index(name=y_axis)
    elif graph_options == "Najetý čas - celkem":
        y_axis = 'duration_minutes'
        filtered=['round_temperature']
        df_graph = filtered_data.groupby(filtered)['duration_min'].sum().reset_index(name=y_axis)    
    elif graph_options == "Počet jízd - hodinový průměr":
        temp_data = filtered_merged_data[["round_temperature", "rental_number"]].groupby("round_temperature").mean().reset_index()
        y_axis = "rental_number"
        df_graph = temp_data



with fig_column:
    fig = px.bar(
        df_graph,
        x='round_temperature',
        y=y_axis, color = "round_temperature",
        color_continuous_scale='darkmint',
        labels={'round_temperature': 'Teplota (°C)', 'duration_min': 'Délka jízdy (min)', 'average_ride_length' : "Průměrná délka jízdy",
            'rides_number' : "Počet jízd", 'total_users' : "Počet uživatelů", 'duration_minutes' : "Celkový čas", "rental_number": "výpůjčky za hodinu"  }
    )

    if graph_options == "Průměrná délka jízdy":
        fig.update_layout(title="Vliv teploty na průměrnou délku jízdy")
    elif graph_options == "Počet jízd - celkem":
        fig.update_layout(title="Vliv teploty na počet jízd")
    elif graph_options == "Počet uživatelů - celkem":
        fig.update_layout(title="Vliv teploty na počet uživatelů")
    elif graph_options == "Najetý čas - celkem":
        fig.update_layout(title="Vliv teploty na celkovou najetou dobu")
    elif graph_options == "Počet jízd - hodinový průměr":
        fig.update_layout(title="Vliv teploty na průměrný hodinový počet jízd")


    st.plotly_chart(fig)
        


#raining
st.subheader("Počet jízd")

rides_with_rain = filtered_data[filtered_data['rain (mm)'] > 0].shape[0]
rides_without_rain = filtered_data[filtered_data['rain (mm)'] == 0].shape[0]

fig_rain = px.bar(
    x=['Jízdy za deště','Jízdy za sucha'],
    y=[rides_with_rain, rides_without_rain],
    color = ['Jízdy za deště','Jízdy za sucha'],
    color_discrete_map = {'Jízdy za deště':'#86C3B3', 'Jízdy za sucha':'#235F73'},
    labels={'x': 'Typ počasí', 'y': 'Počet jízd'},
    title='Počet jízd za deště vs. za sucha'
)
fig_rain.update_layout(legend_title_text= None)

day_rides = filtered_data[filtered_data['is_day']].shape[0]
night_rides = filtered_data[~filtered_data['is_day']].shape[0]

fig_day_night = px.bar(
    x=['Denní jízdy', 'Noční jízdy'],
    y=[day_rides, night_rides],
    color = ['Denní jízdy', 'Noční jízdy'],
    color_discrete_map = {'Denní jízdy':'#86C3B3', 'Noční jízdy':'#235F73'},
    labels={'x': 'Denní doba', 'y': 'Počet jízd'},
    title='Počet jízd během dne vs. v noci'
)
fig_day_night.update_layout(legend_title_text= None)



#alternative graph: with normalization
rain_data = filtered_merged_data[['rental_number', "rain (mm)"]]
rain_data["rain_int"] = rain_data['rain (mm)'].apply(rozdel_uhrn)
intervaly = ['sucho','mírný déšť (do 1 mm)', 'silnější déšť (1 mm a více)' ]
rain_data['sorted_rain_int'] = pd.Categorical(rain_data['rain_int'], categories=intervaly, ordered=True)
rain_data = rain_data[["rental_number", "sorted_rain_int"]].groupby("sorted_rain_int").mean().reset_index()

fig_rain_dry = px.bar(rain_data, x = 'sorted_rain_int', y ='rental_number', color = 'sorted_rain_int', color_discrete_map= {'sucho':'#AADEC4','mírný déšť (do 1 mm)':'#86C3B3', 'silnější déšť (1 mm a více)':'#235F73'})
fig_rain_dry.update_layout(xaxis_title='srážkový úhrn za hodinu', yaxis_title='Průměrný hodinový počet výpůjček', title='Déšť vs. sucho: průměrné hodinové počty výpůjček ')
fig_rain_dry.update_layout(legend_title_text= None)


#rozpad na hodiny
rainy = filtered_merged_data[filtered_merged_data["rain (mm)"] > 0]
dry = filtered_merged_data[filtered_merged_data["rain (mm)"] == 0]
prumer_vypujcek_dry = dry.groupby(dry['time'].dt.hour)['rental_number'].mean()
prumer_vypujcek_rain = rainy.groupby(rainy['time'].dt.hour)['rental_number'].mean()
rentals_rain_time = pd.merge(prumer_vypujcek_dry, prumer_vypujcek_rain, on = "time")
rentals_rain_time.rename(columns={"rental_number_x": "sucho", "rental_number_y": "deštivo"}, inplace=True)
rentals_rain_time.reset_index(inplace=True)
fig_rain_dry_hour = px.line(rentals_rain_time, x='time', y=['sucho', 'deštivo'],color_discrete_sequence=['#86C3B3', '#235F73'],
              labels={'time': 'Hodina', 'value': 'Průměrný hodinový počet výpůjček'},
              title='Déšť vs. sucho: hodinově')
fig_rain_dry_hour.update_layout(legend_title_text= None)


#option for fig
filter_column, middle_spacer, fig_column, back_spacer = st.columns((0.5, 0.2, 0.5, 1))
with filter_column:
    option_fig = st.selectbox(
        'Vyber parametr pro srovnání',
        ('Déšť vs. Sucho celkem', 'Déšť vs. Sucho průměr','Déšť vs. Sucho průměr - hodinově', 'Den vs. Noc')
    )

with fig_column:
    if option_fig == 'Déšť vs. Sucho celkem':
        st.plotly_chart(fig_rain)
    elif option_fig == 'Den vs. Noc':
        st.plotly_chart(fig_day_night)
    elif option_fig == 'Déšť vs. Sucho průměr - hodinově':
        st.plotly_chart(fig_rain_dry_hour)
    elif option_fig == 'Déšť vs. Sucho průměr':
        st.plotly_chart(fig_rain_dry)
