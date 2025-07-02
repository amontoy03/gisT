import streamlit as st  
import folium  
from folium.plugins import Draw 
from streamlit_folium import st_folium 
import geopandas as gpd    
from shapely.geometry import shape
import os 


layer_options = ["Parcels", "Flood Plains", "Zoning", "Streets"]
selected_layers = st.multiselect("Select Available Data", layer_options)


m = folium.Map(location=[35.2271, -80.8431], zoom_start=13)


Draw(
    export=False,
    position="topleft",
    draw_options={
        "polyline": False,
        "circle": False,
        "marker": False,
        "circlemarker": False,
        "rectangle": True,
        "polygon": True,
    },
    edit_options={"edit": True},
).add_to(m)

for layer in selected_layers:
    file_key = layer.lower().replace(" ", "_")
    file_path = os.path.join("data", f"{file_key}.shp")
    

    if os.path.exists(file_path):
        gdf = gpd.read_file(file_path).to_crs("EPSG:4326")
        folium.GeoJson(gdf, name=layer).add_to(m)
    else:
        st.warning(f"Missing: {file_path}")



st_data = st_folium(m, width=1000, height=600)

@st.cache_data
def load_layer(filepath):
    return gpd.read_file(filepath).to_crs("EPSG:4326")

if st_data and st_data.get("all_drawings"):
    drawing = st_data["all_drawings"][-1]
    if drawing and "geometry" in drawing:
        geom = shape(drawing["geometry"])
        st.success("Area selected, displaying data inside:")
        for layer in selected_layers:
            file_key = layer.lower().replace(" ", "_")
            file_path = os.path.join("data", f"{file_key}.shp")
            if os.path.exists(file_path):
                gdf = load_layer(file_path)
                filtered = gdf[gdf.intersects(geom)]
                st.subheader(f"{layer} Features")
                if not filtered.empty:
                    st.dataframe(filtered.drop(columns="geometry").head(10))
                    st.info(f"{len(filtered)} feature(s) found.")
                else:
                    st.warning("No features found in this area.")
            else:
                st.warning(f"Missing: {file_path}")
else:
    st.info("Draw a polygon or rectangle on the map to query features.")