import ee

# Authenticate the Earth Engine API
ee.Authenticate()

# Initialize the Earth Engine API
ee.Initialize()

# Define the region of interest and time period
region = ee.Geometry.Rectangle([77.1025, 28.7041, 77.2979, 28.8789])  # Bounding box for New Delhi
start_date = '2020-01-01'
end_date = '2020-12-31'

# Load Sentinel-2 ImageCollection
sentinel = ee.ImageCollection('COPERNICUS/S2') \
             .filterDate(start_date, end_date) \
             .filterBounds(region)

# Select median composite
sentinel_median = sentinel.median()

# Get the URL for downloading the image
url = sentinel_median.getDownloadURL({
    'scale': 10,
    'region': region,
    'format': 'GeoTIFF'
})

print(url)
