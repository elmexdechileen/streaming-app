import streamlit as st
from cassandra.cluster import Cluster
import pandas as pd

# Connect to Cassandra
cluster = Cluster(["cassandra:9042"])  # Update with your Cassandra cluster address
session = cluster.connect("weather_data")  # Update with your keyspace

# Query to fetch all rows from weather_hourly table
query = "SELECT * FROM weather_hourly"
rows = session.execute(query)

# Convert rows to a pandas DataFrame
df = pd.DataFrame(rows)

# Streamlit app
st.title("Weather Hourly Data")

# Display the DataFrame
st.dataframe(df)
