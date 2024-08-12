import rasterio
import numpy as np

# Paths to the processed NDVI and resampled air pollution data
ndvi_path = 'ndvi.tif'
resampled_air_pollution_path = 'resampled_air_pollution.tif'

# Load the NDVI data
ndvi_data = rasterio.open(ndvi_path)
ndvi = ndvi_data.read(1)

# Load the resampled air pollution data
resampled_air_pollution_data = rasterio.open(resampled_air_pollution_path)
air_pollution = resampled_air_pollution_data.read(1)

# Close the datasets
ndvi_data.close()
resampled_air_pollution_data.close()

from scipy.stats import pearsonr

# Flatten the arrays to 1D for correlation calculation
ndvi_flattened = ndvi.flatten()
air_pollution_flattened = air_pollution.flatten()

# Remove NaN values (if any)
valid_mask = ~np.isnan(ndvi_flattened) & ~np.isnan(air_pollution_flattened)
ndvi_valid = ndvi_flattened[valid_mask]
air_pollution_valid = air_pollution_flattened[valid_mask]

# Calculate Pearson's correlation coefficient
correlation_coefficient, p_value = pearsonr(ndvi_valid, air_pollution_valid)

print(f"Pearson Correlation Coefficient: {correlation_coefficient}")
print(f"P-value: {p_value}")

import matplotlib.pyplot as plt

# Plot NDVI
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.title("NDVI")
plt.imshow(ndvi, cmap='Greens')
plt.colorbar(label='NDVI')

# Plot Air Pollution
plt.subplot(1, 2, 2)
plt.title("Air Pollution")
plt.imshow(air_pollution, cmap='Reds')
plt.colorbar(label='Pollution Level')

plt.tight_layout()
plt.show()

