import streamlit as st
import os
import matplotlib.pyplot as plt
from matplotlib import image
import pandas as pd
import numpy as np
import plotly.express as px

# absolute path to this file
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# absolute path to this file's root directory
PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
# absolute path of directory_of_interest
dir_of_interest = os.path.join(PARENT_DIR, "resources")

IMAGE_PATH = os.path.join(dir_of_interest, "images", "pub.png")
DATA_PATH = os.path.join(dir_of_interest, "data", "open_pubs.csv")

st.title("Welcome - Open Pub Application")

img = image.imread(IMAGE_PATH)
st.image(img)

column_names = ["fsa_id","name","address","postcode","easting","northing","latitude","longitude","local_authority"]
df = pd.read_csv(DATA_PATH)
df.columns=column_names

st.dataframe(df)

df = df.drop_duplicates()
# Replace non-numeric values in the latitude and longitude columns with NaN
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

# Replace NaN values in the latitude and longitude columns with their mean values
df['latitude'] = df['latitude'].fillna(df['latitude'].mean())
df['longitude'] = df['longitude'].fillna(df['longitude'].mean())

# Show basic statistics of the data
st.write('**Basic statistics:**')
st.write(df.describe())

# Show statistics for specific columns
st.write('**Statistics for specific columns:**')
selected_columns = st.multiselect('Select columns', df.columns)
if selected_columns:
    st.write(df[selected_columns].describe())

# Show correlation matrix
st.write('**Correlation matrix:**')
st.write(df.corr())

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.title('Visualization Options')
option = st.sidebar.selectbox('Select a visualization option:', ('Latitude', 'Longitude', 'Address'))

# Create the selected visualization based on the user's choice
if option == 'Latitude':
    # Create a histogram of the latitude values
    st.write('### Latitude')
    st.write('Histogram of latitude values:')
    plt.hist(df['latitude'], bins=30)
    plt.xlabel('Latitude')
    plt.ylabel('Frequency')
    st.pyplot()

elif option == 'Longitude':
    # Create a histogram of the longitude values
    st.write('### Longitude')
    st.write('Histogram of longitude values:')
    plt.hist(df['longitude'], bins=30)
    plt.xlabel('Longitude')
    plt.ylabel('Frequency')
    st.pyplot()

elif option == 'Address':
    # Create a bar chart of the top 10 most common pub addresses
    st.write('### Address')
    st.write('Bar chart of the top 10 most common pub addresses:')
    top_10_addresses = df['address'].value_counts()[:10]
    plt.bar(top_10_addresses.index, top_10_addresses.values)
    plt.xticks(rotation=90)
    plt.xlabel('Address')
    plt.ylabel('Number of pubs')
    st.pyplot()

