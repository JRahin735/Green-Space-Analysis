import osmnx as ox
import geopandas as gpd

# Define the place and type of data to retrieve
place = 'New Delhi, India'
tags = {'landuse': 'recreation_ground'}

# Retrieve the data using the updated function names
green_spaces = ox.features_from_place(place, tags)

# Convert to GeoDataFrame
green_spaces_gdf = gpd.GeoDataFrame(green_spaces)

# Remove fields with invalid types for saving to GeoJSON
for col in green_spaces_gdf.columns:
    if green_spaces_gdf[col].apply(lambda x: isinstance(x, list)).any():
        green_spaces_gdf = green_spaces_gdf.drop(columns=[col])

# Save to a file
green_spaces_gdf.to_file("new_delhi_green_spaces.geojson", driver="GeoJSON")

print(green_spaces_gdf.head())
