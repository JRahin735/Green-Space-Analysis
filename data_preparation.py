import rasterio
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Paths to the .tif files
green_space_path = 'sample1.tif'
air_pollution_path = 'sample2.tif'

# Open the green space data
green_space_data = rasterio.open(green_space_path)
green_space_crs = green_space_data.crs
green_space_transform = green_space_data.transform

# Open the air pollution data
air_pollution_data = rasterio.open(air_pollution_path)
air_pollution_crs = air_pollution_data.crs

# Print metadata for verification
print("Green Space Data CRS:", green_space_crs)
print("Air Pollution Data CRS:", air_pollution_crs)

# Define the resampling method (nearest neighbor)
resample_method = Resampling.nearest

# Define the shape and transform to match the green space data
resampled_air_pollution_data = rasterio.open(
    'resampled_air_pollution.tif',
    'w',
    driver='GTiff',
    height=green_space_data.height,
    width=green_space_data.width,
    count=1,
    dtype=air_pollution_data.dtypes[0],
    crs=green_space_crs,
    transform=green_space_transform,
)

# Perform the resampling
reproject(
    source=rasterio.band(air_pollution_data, 1),
    destination=rasterio.band(resampled_air_pollution_data, 1),
    src_transform=air_pollution_data.transform,
    src_crs=air_pollution_crs,
    dst_transform=green_space_transform,
    dst_crs=green_space_crs,
    resampling=resample_method,
)

# Close the datasets
resampled_air_pollution_data.close()
green_space_data.close()
air_pollution_data.close()

print("Resampling complete. Resampled data saved as 'resampled_air_pollution.tif'.")

# Re-open the green space data
green_space_data = rasterio.open(green_space_path)

# Read the near-infrared (NIR) and red bands (assuming 4-band data)
nir_band = green_space_data.read(4)
red_band = green_space_data.read(3)

# Compute the NDVI
ndvi = (nir_band - red_band) / (nir_band + red_band)

# Save the NDVI as a new GeoTIFF
ndvi_path = 'ndvi.tif'
with rasterio.open(
    ndvi_path,
    'w',
    driver='GTiff',
    height=ndvi.shape[0],
    width=ndvi.shape[1],
    count=1,
    dtype=rasterio.float32,
    crs=green_space_data.crs,
    transform=green_space_data.transform
) as ndvi_dataset:
    ndvi_dataset.write(ndvi.astype(rasterio.float32), 1)

print("NDVI computation complete. NDVI data saved as 'ndvi.tif'.")
