import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bikesharing Brno", page_icon="🚲", layout="wide")
palette = ['#024698', '#c54885', '#e32c83', '#bfa8cc', '#fbf9fc']

st.title('Sdílená kola v Brně')
st.markdown('---')

def load_data():
    df = pd.read_csv("data/23-11-18_15-30_adresses_places_id.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    df = df[~((df['start_time'].dt.month == 4) & (df['start_time'].dt.day >= 1) & (df['start_time'].dt.day <= 10))]

    return df

df_dataset = load_data()
df_dataset["start_time"] = pd.to_datetime(df_dataset["start_time"], format="%Y-%m-%d %H:%M:%S")

df_weather = pd.read_csv('data/weather/weather-22-to-05-11-23.csv')
df_weather["time"] = pd.to_datetime(df_weather["time"], format="%Y-%m-%dT%H:%M")

st.sidebar.header("👇 Filtrovací panel")

# year
years = df_dataset["year"].unique()
selected_years = st.sidebar.multiselect('Vyber rok', years,years)

df_dataset['is_day'] = df_dataset['is_day ()'].astype(bool)

filtered_data = df_dataset[df_dataset["year"].isin(selected_years)]


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

filter_column, middle_spacer, fig_column, back_spacer = st.columns((0.5, 0.2, 0.5, 1))

with filter_column:
    graph_options = st.selectbox("Vyber metriku", ("Průměrná délka jízdy", "Počet jízd", "Počet uživatelů","Najetý čas"))
    filtered=''
    if graph_options == "Průměrná délka jízdy":
        y_axis = 'average_ride_length'
        filtered=['round_temperature']
        df_graph = filtered_data.groupby(filtered)['duration_min'].mean().reset_index(name=y_axis)
    elif graph_options == "Počet jízd":
        y_axis = 'rides_number'
        filtered=['round_temperature']
        df_graph = filtered_data.groupby(filtered).size().reset_index(name=y_axis)
    elif graph_options == "Počet uživatelů":
        y_axis = 'total_users'
        filtered=['round_temperature']
        df_graph = filtered_data.groupby(filtered)['user_id'].nunique().reset_index(name=y_axis)
    elif graph_options == "Najetý čas":
        y_axis = 'duration_minutes'
        filtered=['round_temperature']
        df_graph = filtered_data.groupby(filtered)['duration_min'].sum().reset_index(name=y_axis)

with fig_column:

    fig = px.bar(
        df_graph,
        x='round_temperature',
        y=y_axis,
        labels={'round_temperature': 'Teplota (°C)', 'duration_min': 'Délka jízdy (min)', 'average_ride_length' : "Průměrná délka jízdy",
            'rides_number' : "Počet jízd", 'total_users' : "Počet uživatelů", 'duration_minutes' : "Celkový čas"    }
    )

    if graph_options == "Průměrná délka jízdy":
       fig.update_layout(title="Vliv teploty na průměrnou délku jízdy")
    elif graph_options == "Počet jízd":
        fig.update_layout(title="Vliv teploty na počet jízd")
    elif graph_options == "Počet uživatelů":
        fig.update_layout(title="Vliv teploty na počet uživatelů")
    elif graph_options == "Najetý čas":
        fig.update_layout(title="Vliv teploty na celkovou najetou dobu")

    st.plotly_chart(fig)

#raining
st.subheader("Počet jízd")

rides_with_rain = filtered_data[filtered_data['rain (mm)'] > 0].shape[0]
rides_without_rain = filtered_data[filtered_data['rain (mm)'] == 0].shape[0]

fig_rain = px.bar(
    x=['Jízdy za deště','Jízdy za sucha'],
    y=[rides_with_rain, rides_without_rain],
    labels={'x': 'Typ počasí', 'y': 'Počet jízd'},
    title='Počet jízd za deště vs. za sucha'
)

day_rides = filtered_data[filtered_data['is_day']].shape[0]
night_rides = filtered_data[~filtered_data['is_day']].shape[0]

fig_day_night = px.bar(
    x=['Denní jízdy', 'Noční jízdy'],
    y=[day_rides, night_rides],
    labels={'x': 'Denní doba', 'y': 'Počet jízd'},
    title='Počet jízd během dne vs. v noci'
)

# data merge

df_dataset.set_index('start_time', inplace=True)

df_dataset['rental_number'] = 1

rentals_in_hours = df_dataset['rental_number'].resample('H').sum()
merged_data = pd.merge(rentals_in_hours, df_weather, how = "left", left_on = "start_time", right_on = "time" )

merged_data["rain_yes_no"] = True
mask = merged_data["rain (mm)"] == 0
merged_data.loc[mask, "rain_yes_no"] = False

mean_rain = merged_data[merged_data["rain_yes_no"]]['rental_number'].mean().round(0)
mean_dry = merged_data[~merged_data["rain_yes_no"]]['rental_number'].mean().round(0)

data_for_plot = {
    'Kategorie': ['Deštivé hodiny', 'Nedeštivé hodiny'],
    'Průměrný počet výpůjček': [mean_rain, mean_dry]
}

df_for_plot = pd.DataFrame(data_for_plot)
fig_rain_dry = px.bar(df_for_plot, x='Kategorie', y='Průměrný počet výpůjček', barmode='group')
fig_rain_dry.update_layout(xaxis_title='Kategorie', yaxis_title='Průměrný počet výpůjček', title='Průměr výpůjček podle počasí')


#option for fig
filter_column, middle_spacer, fig_column, back_spacer = st.columns((0.5, 0.2, 0.5, 1))
with filter_column:
    option_fig = st.selectbox(
        'Vyber parametr pro srovnání',
        ('Déšť vs. Sucho celkem', 'Déšť vs. Sucho průměr', 'Den vs. Noc')
    )

with fig_column:
    if option_fig == 'Déšť vs. Sucho celkem':
        st.plotly_chart(fig_rain)
    elif option_fig == 'Den vs. Noc':
        st.plotly_chart(fig_day_night)
    elif option_fig == 'Déšť vs. Sucho průměr':
        st.plotly_chart(fig_rain_dry)
