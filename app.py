import json
import os

import streamlit as st
import folium
from folium.plugins import Draw
from shapely.geometry import shape
from streamlit_folium import st_folium
import pandas as pd


layers = st.multiselect(
    "Select Available Data",
    ["Parcels", "Zoning", "Streets", "Flood Plains"],
)

m = folium.Map(location=[35.2271, -80.8431], zoom_start=13)
m.add_child(folium.LatLngPopup())

Draw(
    export=True,
    filename='drawn.geojson',
    position='topleft',
    draw_options={
        'polyline': False,
        'circle': False,
        'marker': False,
        'circlemarker': False,
        'rectangle': True,
        'polygon': True
    },
    edit_options={"edit": True},
).add_to(m)

st_data = st_folium(m, width=1000, height=600)

if st_data and st_data.get("last_active_drawing"):

    selected_geom = shape(st_data["last_active_drawing"]["geometry"])
    st.success("Area selected! Displaying data inside:")

    for layer in layers:
        file_key = layer.lower().replace(" ", "_")
        filepath = os.path.join("data", f"{file_key}.geojson")

        if os.path.exists(filepath):
            try:
                with open(filepath) as f:
                    data = json.load(f)

                rows = []
                for feature in data.get("features", []):
                    geom = shape(feature.get("geometry"))
                    if geom.intersects(selected_geom):
                        rows.append(feature.get("properties", {}))

                st.subheader(f"{layer} Inside Selected Area")
                if rows:
                    st.dataframe(pd.DataFrame(rows))
                    st.info(f"{len(rows)} feature(s) found.")
                else:
                    st.warning("No features found in this area.")
            except Exception as e:
                st.error(f"Error loading {file_key}: {e}")
        else:
            st.warning(f"Missing file: {file_key}.geojson")
else:
    st.info("Draw a polygon or rectangle on the map to display data.")
