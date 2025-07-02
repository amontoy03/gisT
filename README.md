# GIS Selection App

This repository contains a simple Streamlit application that lets users
select from several GIS datasets and draw an area on an interactive map
in order to see which features fall inside the selected area.

## Features

- Choose which layers to display (Parcels, Zoning, Streets, Flood Plains).
- Draw a polygon or rectangle on the map.
- See tabular information for features that intersect the drawn area.

The sample data included in the `data/` directory is provided in GeoJSON
format and is meant for demonstration only.

## Running

Install the required packages and start Streamlit:

```bash
pip install -r requirements.txt
streamlit run app.py
```

A browser window will open with the interactive map. Select any layers,
draw a shape on the map, and the corresponding data will be displayed.

