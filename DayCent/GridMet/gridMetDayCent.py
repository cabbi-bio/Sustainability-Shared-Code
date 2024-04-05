import os
import sys
import wget
import xarray as xr
import netCDF4
import numpy as np
import pandas as pd

# This is a Python script that will download minimum temperature, maximum temperature, precipitation, solar radiation, wind speed, and relative humidity.
# # It will then process the data so it is in the netCDF format needed to be input in DayCent. It is customizable based on the years and spatial domain needed. Also the directory you want to download the data into 
# is an input. 
# This was developed off a script provided by Theo Hartman from the Heaton Lab at Illinois. 
# For questions, email Leslie Stoecker, lensor@illinois.edu 

# Get the arguments passed through command line - uncomment if using 
syr, eyr, latitude, longitude, dir, locations, delim = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]

# Inputs to change for only a single latitude/longitude point. Remove the # from the start of the following 7 lines
#syr = 2020 # First year to pull data. The first year in the dataset is 1979
#eyr = 2020 # Last year to pull data. There is current data, but it is not finalized currently.
#latitude = 40.06 # Latitude of the point of interest
#longitude = -88.20 # Longitude of the point of interest
#dir = 'C:\\Users\\IGB\\Box\\Sustainability Hub\\GridMet Data Download\\' # Directory where all the files will be stored
#locations = 'Energy_farm' #File Naming of location for now only. Can implement multiple sites later if needed.    
#delim = '\\' # Customizable file/directory delimiter depending on the system you are running it on

    
# Changes all the inputs to numbers
latitude = float(latitude)
longitude = float(longitude)
y = int(syr)

# Create folders if they do not exist
# First location to put the full data files
NWK_vars = ['tmmn','tmmx','pr','srad','vs','rmax','rmin']
for v in NWK_vars:
    var_dir = dir + delim + v
    if not os.path.exists(var_dir):
        os.makedirs(var_dir)

# Location to put the DayCent output data files
output_dir = dir + delim + 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

var_dir = output_dir + delim + locations
if not os.path.exists(var_dir):
    os.makedirs(var_dir)

# Loop through the years needed
while y<=int(eyr):

# Minimum Air Temperature: 
    url = 'http://www.northwestknowledge.net/metdata/data/tmmn' + '_' + str(y) + '.nc'
    file = dir + delim + 'tmmn' + delim + 'tmmn_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)
    
    temp_min = xr.open_dataset(file)
    temp_min = temp_min.sel(lat=latitude, lon=longitude,method = 'nearest')
    temp_min = temp_min.rename({'day':'time'})
    temp_min = temp_min.rename({'air_temperature':'tmmn'})
    temp_min = temp_min.tmmn - 273.15
    temp_min = temp_min.to_dataset()
    temp_min = temp_min.astype('double')
    temp_min.tmmn.attrs['units'] = 'deg C'
    temp_min_array = temp_min.tmmn.to_numpy()
    temp_min_array = np.round_(temp_min_array, decimals = 4)
    xr.Dataset.close(temp_min)
    print('Finished: '  + str(y) + ' Minimum Temperature')

    # Maximum Air Temperature: 
    url = 'http://www.northwestknowledge.net/metdata/data/tmmx' + '_' + str(y) + '.nc'
    file = dir + delim +'tmmx' + delim + 'tmmx_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)

    temp_max = xr.open_dataset(file)
    temp_max = temp_max.sel(lat=latitude, lon=longitude,method = 'nearest')
    temp_max = temp_max.rename({'day':'time'})
    temp_max = temp_max.rename({'air_temperature':'tmax'})
    temp_max = temp_max.tmax - 273.15
    temp_max = temp_max.to_dataset()
    temp_max = temp_max.astype('double')
    temp_max.tmax.attrs['units'] = 'deg C'
    temp_max_array = temp_max.tmax.to_numpy()
    temp_max_array = np.round_(temp_max_array, decimals = 4)
    xr.Dataset.close(temp_max)
    print('Finished: ' + str(y) + ' Maximum Temperature')

    # Daily Precipitaiton Accumulation:
    url = 'http://www.northwestknowledge.net/metdata/data/pr' + '_' + str(y) + '.nc'
    file = dir + delim + 'pr' + delim + 'pr_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)

    precip = xr.open_dataset(file)
    precip = precip.sel(lat=latitude, lon=longitude,method = 'nearest')
    precip = precip.rename({'day':'time'})
    precip = precip.rename({'precipitation_amount':'prec'})
    precip = precip.astype('double')
    precip = precip.prec * 0.1 #Convert to cm from mm
    precip_array = precip.to_numpy()
    precip_array = np.round_(precip_array, decimals = 4)
    xr.Dataset.close(precip)
    print('Finished: ' + str(y) + ' Precipitation')
 
# Surface Downwelling Shortwave Radiation: Output will be rads_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/srad' + '_' + str(y) + '.nc'
    file = dir + delim + 'srad' + delim + 'srad_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)

    radiation = xr.open_dataset(file)
    radiation = radiation.sel(lat=latitude, lon=longitude,method = 'nearest')
    radiation = radiation.rename({'day':'time'})
    radiation = radiation.rename({'surface_downwelling_shortwave_flux_in_air':'rads'})
    radiation = radiation.astype('double')
    radiation = radiation.rads / 0.484582 #Conversion from W/m2 to Langley/day
    radiation_array = radiation.to_numpy()
    radiation_array = np.round_(radiation_array, decimals = 4)
    xr.Dataset.close(radiation)
    print('Finished: ' + str(y) + ' Solar Radiation')

    # Wind Speed: Output will be wspd_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/vs' + '_' + str(y) + '.nc'
    file = dir + delim + 'vs' + delim + 'vs_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)

    wind = xr.open_dataset(file)
    wind = wind.sel(lat=latitude, lon=longitude,method = 'nearest')
    wind = wind.rename({'day':'time'})
    wind = wind.rename({'wind_speed':'wspd'})
    wind = wind.astype('double')
    wind = wind.wspd * 2.23694 #Conversion from m/s to mph
    wind_array = wind.to_numpy()
    wind_array = np.round_(wind_array, decimals = 4)
    xr.Dataset.close(wind)
    print('Finished: ' + str(y) + ' Wind Speed')

    # Maximum Relative Humidity: Output will be relh_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/rmax' + '_' + str(y) + '.nc'
    file = dir + delim + 'rmax' + delim + 'rmax_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)

    rhmx = xr.open_dataset(file)
    rhmx = rhmx.sel(lat=latitude, lon=longitude,method = 'nearest')
    rhmx = rhmx.rename({'day':'time'})
    rhmx = rhmx.rename({'relative_humidity':'relh'})
    rhmx = rhmx.astype('double')
    rhmx.relh.attrs['units'] = 'percent'
    xr.Dataset.close(rhmx)
    print('Finished: '  + str(y) + ' Maximum Relative Humidity')

    # Minimum Relative Humidity: Output will be relh_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/rmin_' + str(y) + '.nc'
    file = dir + delim + 'rmin' + delim + 'rmin_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)

    rhmn = xr.open_dataset(file)
    rhmn = rhmn.sel(lat=latitude, lon=longitude,method = 'nearest')
    rhmn = rhmn.rename({'day':'time'})
    rhmn = rhmn.rename({'relative_humidity':'relh'})
    rhmn = rhmn.astype('double')
    rhmn.relh.attrs['units'] = 'percent'
    xr.Dataset.close(rhmn)
    print('Finished: '  + str(y) + ' Minimum Relative Humidity')

    #Average Relative Humidity: Output is relh_yyyy.nc
    rh_ave = (rhmn.relh+rhmx.relh)/2
    rh_ave_array = rh_ave.to_numpy()
    rh_ave_array = np.round_(rh_ave_array, decimals = 4)
    print('Finished: ' + str(y) + ' Average Relative Humidity')

    #Put together time coordinates
    day = precip.time.dt.day.to_numpy()
    month = precip.time.dt.month.to_numpy()
    year = precip.time.dt.year.to_numpy()
    doy = precip.time.dt.dayofyear.to_numpy()   

    #Create dataframe with all needed data for DayCent
    output_dataframe = pd.DataFrame([day,month,year,doy,temp_max_array,temp_min_array,precip_array,radiation_array,rh_ave_array,wind_array]).transpose()

    #Write weather data to text file formatted
    output_file = dir + delim + 'DayCent_weather_' + locations + '_' + str(y) + '.txt'
    print(output_file)
    output_dataframe[0] = output_dataframe[0].astype(int)
    output_dataframe[1] = output_dataframe[1].astype(int)
    output_dataframe[2] = output_dataframe[2].astype(int)
    output_dataframe[3] = output_dataframe[3].astype(int)
    output_dataframe.to_csv(output_file, sep='\t', index=False, header=False)

    print('Finished: ' + str(y) + ' Writing Output File')

    y = y+1