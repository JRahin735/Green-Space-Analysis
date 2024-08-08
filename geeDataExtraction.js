// Ran on the Google Earth Engine Console

// Define the region of interest (New Delhi)
var region = ee.Geometry.Rectangle({
  coords: [[77.1025, 28.7041], [77.2979, 28.8789]],
  geodesic: false
});

// Define the time period for the imagery
var startDate = '2020-01-01';
var endDate = '2020-12-31';

// Load Sentinel-2 ImageCollection and filter by date and region
var sentinel = ee.ImageCollection('COPERNICUS/S2')
                .filterDate(startDate, endDate)
                .filterBounds(region)
                .select(['B2', 'B3', 'B4', 'B8']);  // Select common bands (Blue, Green, Red, NIR)

// Create a median composite of the selected images
var sentinelMedian = sentinel.median().clip(region);

// Define visualization parameters
var visParams = {
  bands: ['B4', 'B3', 'B2'],  // True color (RGB)
  min: 0,
  max: 3000,
  gamma: 1.4
};

// Add the median composite to the map
Map.centerObject(region, 11);
Map.addLayer(sentinelMedian, visParams, 'Sentinel-2 Median Composite');

// Export the image to Google Drive
Export.image.toDrive({
  image: sentinelMedian,
  description: 'NewDelhi_Sentinel_Median_2020',
  folder: 'EarthEngineExports',
  region: region,
  scale: 10,  // 10 meters per pixel
  maxPixels: 1e9
});
