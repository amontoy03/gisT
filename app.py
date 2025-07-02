import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import shape, box
import os


layers = st.multiselect("Select Available Data", ["Parcels", "Flood Plains", "Zoning", "Streets"])

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
    edit_options={'edit': True}
).add_to(m)

st_data = st_folium(m, width=1000, height=600)

if st_data and st_data.get("last_active_drawing"):
    geojson = st_data["last_active_drawing"]["geometry"]
    selected_geom = shape(geojson)
    st.success("Area selected! Displaying data inside:")

    for layer in layers:
        file_key = layer.lower().replace(" ", "_")
        filepath = os.path.join("data", f"{file_key}.shp")

        if os.path.exists(filepath):
            try:
                gdf = gpd.read_file(filepath).to_crs("EPSG:4326")
                filtered = gdf[gdf.intersects(selected_geom)]

                st.subheader(f"{layer} Inside Selected Area")
                if not filtered.empty:
                    st.dataframe(filtered.drop(columns="geometry").head(10))
                    st.info(f"{len(filtered)} feature(s) found.")
                else:
                    st.warning("No features found in this area.")
            except Exception as e:
                st.error(f"Error loading {file_key}: {e}")
        else:
            st.warning(f"Missing file: {file_key}.shp")
else:
    st.info("Draw a polygon or rectangle on the map to display data.")