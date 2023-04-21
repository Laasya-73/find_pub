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

st.title("Welcome - Find the Nearest Pub")

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

st.sidebar.title('Map Options')
option = st.sidebar.selectbox('Select a map option:', ('Postal Code', 'Local Authority'))

# Get the relevant data based on the user's choice
if option == 'Postal Code':
    # Get a list of unique postcode areas in the dataset
    postcode_areas = df['postcode'].str.extract(r'^([A-Z]{1,2}\d{1,2}[A-Z]?)')[0].unique()
    # Ask the user to choose a postcode area
    selected_postcode = st.sidebar.selectbox('Select a postcode area:', postcode_areas)
    # Filter the dataframe to only include pubs in the selected postcode area
    filtered_df = df[df['postcode'].str.startswith(selected_postcode)]
else:
    # Get a list of unique local authorities in the dataset
    authorities = df['local_authority'].unique()
    # Ask the user to choose a local authority
    selected_authority = st.sidebar.selectbox('Select a local authority:', authorities)
    # Filter the dataframe to only include pubs in the selected local authority
    filtered_df = df[df['local_authority'] == selected_authority]

# Display a map of the filtered data
st.write('### Map')
st.map(filtered_df)