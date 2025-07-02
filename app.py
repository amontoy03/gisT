import streamlit as st  
import folium  
from folium.plugins import Draw 
from streamlit_folium import st_folium 
import geopandas as gpd    
from shapely.geometry import shape
import os 

# let user pick a data layer to display on the map
layer_options = ["Parcels", "Flood Plains", "Zoning", "Streets"]
selected_layers = st.multiselect("Select Available Data", layer_options)

# Create a Folium map centered on Charlotte, NC
m = folium.Map(location=[35.2271, -80.8431], zoom_start=13)

# Add a toolbar to draw polygons and rectangles
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

# Converts Flood Plains to flood_plains and looks for data/flood_plains.shp
# Reads and Converts the shapefile to EPSG:4326
for layer in selected_layers:
    file_key = layer.lower().replace(" ", "_")
    file_path = os.path.join("data", f"{file_key}.shp")
    

    if os.path.exists(file_path):
        gdf = gpd.read_file(file_path).to_crs("EPSG:4326")
        folium.GeoJson(gdf, name=layer).add_to(m)
    else:
        st.warning(f"Missing: {file_path}")


# Embeds the Folium map in the Streamlit app
st_data = st_folium(m, width=1000, height=600)

# Avoids reloading the shapefile every time
@st.cache_data
def load_layer(filepath):
    return gpd.read_file(filepath).to_crs("EPSG:4326")


if st_data and st_data.get("all_drawings"):
    drawing = st_data["all_drawings"][-1]
    if drawing and "geometry" in drawing:
        geom = shape(drawing["geometry"])
        st.success("Area selected! Displaying data inside:")
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

# If no drawing is made, prompt the user
else:
    st.info("Draw a polygon or rectangle on the map to query features.")