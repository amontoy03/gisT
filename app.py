import streamlit as st
import folium
from streamlit_folium import st_folium

layers = st.multiselect("Select Available Data", ["Parcels", "Flood Plains", "Zoning", "Streets"])

m = folium.Map(location=[35.2271, -80.8431], zoom_start=13)
m.add_child(folium.LatLngPopup())

st_folium(m, width=1000, height=600)