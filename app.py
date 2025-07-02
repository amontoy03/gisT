import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import os


layer_options = ["Parcels", "Flood Plains", "Zoning", "Streets"]
selected_layers = st.multiselect("Select Available Data", layer_options)


m = folium.Map(location=[35.2271, -80.8431], zoom_start=13)
m.add_child(folium.LatLngPopup())

for layer in selected_layers:
    file_key = layer.lower().replace(" ", "_")
    file_path = os.path.join("data", f"{file_key}.shp")
    
    if os.path.exists(file_path):
        gdf = gpd.read_file(file_path)
        folium.GeoJson(gdf, name=layer).add_to(m)
    else:
        st.warning(f"Missing: {file_path}")


st_folium(m, width=1000, height=600)