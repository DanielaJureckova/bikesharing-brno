import pandas as pd
from sklearn.cluster import KMeans

# Sample DataFrame with latitude and longitude columns
data = pd.read_csv("next_rekola_both.csv")

df = pd.DataFrame(data)
# Create a K-Means clustering model
kmeans = KMeans(n_clusters=1000, n_init = 10)

# Fit the model to the data
df['Cluster'] = kmeans.fit_predict(df[['start_latitude', 'start_longitude']])

# Calculate the cluster centers (positions of stations)
station_positions = df.groupby('Cluster')[['start_latitude', 'start_longitude']].mean()
station_positions.reset_index(inplace=True)


# Spočtěte počet dat v každém klastru
cluster_counts = df['Cluster'].value_counts().reset_index()
cluster_counts.columns = ['Cluster', 'Count']

# Spočtěte celkový počet dat
total_count = len(df)

# Vytvořte sloupec s procenty
cluster_counts['Percentage'] = (cluster_counts['Count'] / total_count) * 100


station_positions.to_csv("data_test2.csv", index = False)