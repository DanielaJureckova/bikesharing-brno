import streamlit as st
import pandas as pd
import plotly.express as px

#page settings
st.set_page_config(page_title="Bikesharing Brno", page_icon="🚲", layout="wide")

st.title("Sdílená kola v Brně")
st.subheader("od jara do podzimu")
st.markdown('---')

#data load
def load_data():
    df = pd.read_csv("Data/23-11-17_19-00_address+places_id.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    return df

df_dataset = load_data()

#filter
st.sidebar.header("👇 Filtrovací panel")

years = df_dataset["year"].unique()
selected_years = st.sidebar.multiselect('Vyber rok', years, years)

filtered_data = df_dataset[df_dataset["year"].isin(selected_years)]

#graph
st.subheader("Celkový počet jízd")
filtered_data['date'] = pd.to_datetime(filtered_data['month_year'], format='%m/%y')
df_graph = filtered_data.groupby(['month_year', 'company']).size().reset_index(name='počet')
    
df_graph['date'] = pd.to_datetime(df_graph['month_year'], format='%m/%y')
df_sorted = df_graph.sort_values(by='date')
fig = px.line(df_sorted, x='month_year', y='počet', color='company',
                title='Počet jízd v čase',
                labels={'month_year': 'Datum', 'company': 'Společnost', 'počet': 'Počet jízd'},
                color_discrete_map={'nextbike': 'blue', 'rekola': '#FF69B4'})
    
st.plotly_chart(fig)




