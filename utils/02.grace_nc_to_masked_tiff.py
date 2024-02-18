# !pip install rioxarray >> /dev/null

import xarray as xr
import rioxarray as rio

from google.colab import drive
drive.mount('/content/drive')

# Open the GRACE_GRACE-FO_Mascon dataset
path = '/content/drive/MyDrive/Colab Notebooks/FAO Analysis/data/CSR_GRACE_GRACE-FO_RL0602_Mascons_all-corrections.nc'
ds = xr.open_dataset(path)

# Extract latitude, longitude, and time dimensions
lat = ds['lat'].values
lon = ds['lon'].values
time = ds['time'].values
# Get dimensions
height, width = len(lat), len(lon)

def _coordAssign(xrData):
  # convert longitude from (0-360) to (-180 to 180) (if required)
  xrData['lon'] = (xrData['lon'] + 180) % 360 - 180
  xrData = xrData.sortby(xrData.lon)
  xrData = xrData.rio.set_spatial_dims('lon', 'lat')
  xrData.rio.set_crs("epsg:4326")                             ## print(data.rio.crs) #if CRS isn't discovered or None, add CRS using data.rio.set_crs(<YOUR EPSG>) 
  return xrData

# Land mask layer  
mask = True
nodata_value = np.nan
if mask==True:
  path_mask = '/content/drive/MyDrive/Colab Notebooks/FAO Analysis/data/CSR_GRACE_GRACE-FO_RL06_Mascons_v02_LandMask.nc'
  ds_mask = xr.open_dataset(path_mask)
  ds_mask1 = xr.where(ds_mask == 0, nodata_value, ds_mask)
  ds_mask2 = _coordAssign(ds_mask1)                              ## Assign Coordinates
  # <DATA-NAME>.rio.to_raster(f"/content/LANDMASK/landmask.tif") ## To export mask as geotiff

# To mask out ocean
def maskFunc(toClip, ds_mask = ds_mask):
  return xr.where(ds_mask==1, toClip, float('nan'))

# Iterate over each time step
for i, t in enumerate(time):
  # Extract data for the current time step
  data = ds['lwe_thickness'][i]

  if mask == True:
    data = maskFunc(data) 
  data = _coordAssign(data)                                       ## Assign Coordinates                      

  # Construct the output file name
  pre_date = time_time_bounds['time_beginning_YMD'][i]
  post_date = time_time_bounds['time_end_YMD'][i]
  output_filename = f"/content/GRACE/{pre_date}_{post_date}.tif"  ## You can adjust the file naming convention as needed
  data.rio.to_raster(output_filename)

# Zip the data folder
!zip -r GRACE.zip /content/GRACE/*.tif >> /dev/null
# Source: https://pratiman-91.github.io/2020/08/01/NetCDF-to-GeoTIFF-using-Python.html