#from numpy.lib.arraysetops import union1d_dispatcher
import pandas as pd
import streamlit as st
#from PIL import Image
#import plotly.express as px
#import base64
#import numpy as np
#import isochrones
from streamlit_folium import folium_static
#from branca.element import Template, MacroElement
import folium
#from settings import template

# Set page title and favicon.
TRAIN__ICON_URl= 'resources/img/train_icon.png'

# Page layout
## adds page icon and Page expands to full width
st.set_page_config(
    page_title="Train Station Isochrones", page_icon=TRAIN__ICON_URl,
    layout="wide",
)
###Load Relevant Data###


##Loads image for 
#image = Image.open('../resources/img/DSC09499.JPG')

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

## Station Location
response = supabase.table('stations').select("*").execute()
data,_ = response
data_all = pd.DataFrame(data[1])

selected_data = data_all[data_all['region']=="Klang Valley"]

st.header(f'Klang Valley Train Stations Isochrone Data')
st.write("""
***
""")

# Create a new DataFrame where each latitude and longitude pair is unique
unique_stations = selected_data.drop_duplicates(subset=['latitude', 'longitude'])
# Create a map centered around the average latitude and longitude of the stations
mapped = folium.Map(location=[unique_stations['latitude'].mean(), unique_stations['longitude'].mean()], zoom_start=13)

# Add a marker for each station
for _, station in unique_stations.iterrows():
    folium.Marker(location=[station['latitude'], station['longitude']], 
                popup=f"{station['name']} ({station['station_id']})").add_to(mapped)

# Display the map
folium_static(mapped, width=st.sidebar.slider("Width", min_value=600, max_value=2000, value=960), height=600)

#Display dataframe
st.dataframe(selected_data)

#download data
csv = selected_data.to_csv().encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'Klang_Valley_data.csv',
    mime='text/csv'
    )

##Entrance Data
response = supabase.table('entrances').select("*").execute()
data,_ = response
selected_data = pd.DataFrame(data[1])


st.header(f'Klang Valley Train Stations Entrances')
st.write("""
***
""")

# Create a new DataFrame where each latitude and longitude pair is unique
unique_stations = selected_data.drop_duplicates(subset=['latitude', 'longitude'])
# Create a map centered around the average latitude and longitude of the stations
mapped = folium.Map(location=[unique_stations['latitude'].mean(), unique_stations['longitude'].mean()], zoom_start=13)

# Add a marker for each station
for _, station in unique_stations.iterrows():
    folium.Marker(location=[station['latitude'], station['longitude']], 
                popup=f"({station['entrance_id']})").add_to(mapped)

# Display the map
folium_static(mapped, width=st.sidebar.slider("Width Map 2", min_value=600, max_value=2000, value=960), height=600)

#Display dataframe
st.dataframe(selected_data)

#download data
csv = selected_data.to_csv().encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'Klang_Valley_Entrances_data.csv',
    mime='text/csv'
    )

