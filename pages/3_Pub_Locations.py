import streamlit as st
import os
import pandas as pd
from matplotlib import image
import numpy as np
from scipy.spatial.distance import cdist

# absolute path to this file
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# absolute path to this file's root directory
PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
# absolute path of directory_of_interest
dir_of_interest = os.path.join(PARENT_DIR, "resources")

IMAGE_PATH = os.path.join(dir_of_interest, "images", "pub.png")
DATA_PATH = os.path.join(dir_of_interest, "data", "open_pubs.csv")

st.title("Welcome - Find the Pub Locations")

img = image.imread(IMAGE_PATH)
st.image(img)

column_names = ["fsa_id","name","address","postcode","easting","northing","latitude","longitude","local_authority"]
df = pd.read_csv(DATA_PATH)
df.columns=column_names

df = df.drop_duplicates()
# Replace non-numeric values in the latitude and longitude columns with NaN
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

# Replace NaN values in the latitude and longitude columns with their mean values
df['latitude'] = df['latitude'].fillna(df['latitude'].mean())
df['longitude'] = df['longitude'].fillna(df['longitude'].mean())

st.write('### Find the nearest pubs to your location')
lat = st.number_input('Enter your latitude:', value=51.5074)
lon = st.number_input('Enter your longitude:', value=-0.1278)

# Calculate the distances between the user's location and each pub using Euclidean distance
user_location = np.array([[lat, lon]])
pub_locations = df[['latitude', 'longitude']].to_numpy()
distances = cdist(user_location, pub_locations, metric='euclidean')[0]

# Get the indices of the 5 nearest pubs
nearest_indices = np.argsort(distances)[:5]

# Create a new dataframe containing only the nearest pubs
nearest_pubs = df.iloc[nearest_indices]

# Display a map of the nearest pubs
st.write('### Map of the nearest pubs')
st.map(nearest_pubs)

# Display a table of the nearest pubs
st.write('### Nearest pubs')
st.table(nearest_pubs[['name', 'address', 'postcode']])