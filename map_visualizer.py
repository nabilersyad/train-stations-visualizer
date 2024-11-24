#from numpy.lib.arraysetops import union1d_dispatcher
import pandas as pd
import streamlit as st
import geopandas as gpd
import os
import folium
from streamlit_folium import folium_static
from shapely.geometry import shape
from supabase import create_client, Client

# Set page title and favicon.
icon_url= 'resources/img/webapp_logo.png'

# Page layout
## Adds page icon and Page expands to full width
st.set_page_config(
    page_title="Train Station Isochrones", page_icon=icon_url,
    layout="wide",
)

## Set up supabase Client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

## Load Station Location
response = supabase.table('stations').select("*").execute()
data,_ = response
data_all = pd.DataFrame(data[1])

data_klang_valley = data_all[data_all['region']=="Klang Valley"]

st.header(f'Klang Valley Train Stations Isochrone Data')
st.write("""
***
""")
isochrone_size = 300
# Create a new DataFrame where each latitude and longitude pair is unique
unique_stations = data_klang_valley.drop_duplicates('station_code')


###Page Layout

left_column, right_column = st.columns([1, 4])
# You can use a column just like st.sidebar:
with left_column:
    width = st.slider("Width", min_value=600, max_value=2000, value=960)
    isochrone_size = st.radio(
        "Isochrone Size",
        options= [300,600,900],
        captions= ["5 Minutes", "10 Minutes", "15 Minutes"],
        index=0,
        horizontal=False
) 
    
# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    # Create a map centered around the average latitude and longitude of the stations
    mapped = folium.Map(location=[unique_stations['latitude'].mean(), unique_stations['longitude'].mean()], 
                        zoom_start=12)



    ## Load isochrone data
    response_isochrones = supabase.table('station_isochrones').select("*").execute()
    data,_ = response_isochrones
    data_klang_valley_isochrones = pd.DataFrame(data[1])
    data_klang_valley_isochrones = data_klang_valley_isochrones[data_klang_valley_isochrones['value'] == isochrone_size]

    # Convert the geometry column from dictionaries to shapely Polygons
    data_klang_valley_isochrones['geometry'] = data_klang_valley_isochrones['geometry'].apply(lambda geom: shape(geom))

    # Convert the DataFrame to a GeoDataFrame
    data_klang_valley_isochrones = gpd.GeoDataFrame(data_klang_valley_isochrones, geometry='geometry', crs='EPSG:4326')
        
        # Add a marker for each station
    for _, station in unique_stations.iterrows():
        folium.Marker(location=[station['latitude'], station['longitude']], 
                    popup=f"{station['name']} ({station['station_id']})").add_to(mapped)
    # Add GeoDataFrame geometries to the map
    folium.GeoJson(
        data_klang_valley_isochrones,
        name="Entrances Isochrones",
        style_function=lambda feature: {
            'fillColor': 'cyan',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        }
    ).add_to(mapped)
    # Add a layer control panel
    folium.LayerControl().add_to(mapped)

    folium_static(mapped, width=width, height=600)

#Display dataframe
st.dataframe(data_klang_valley)

#download data
csv = data_klang_valley.to_csv().encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'Klang_Valley_data.csv',
    mime='text/csv'
    )


#Display dataframe
st.dataframe(data_klang_valley_isochrones)

#download data
csv = data_klang_valley_isochrones.to_csv().encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'Klang_Valley_Stations_isochrones_data.csv',
    mime='text/csv'
    )

