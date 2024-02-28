
import os
import sys
import wget
import xarray as xr
import netCDF4

# This is a Python script that will download minimum and maximum air temperature, precipitation, solar radiation, wind speed, and minimum, maximum and average relative humidity GridMet data.
# It will then process the data so it is in the netCDF format needed to be input in AgroIBIS. It is customizable based on the years and spatial domain needed. Also the directory you want to download the data into 
# is an input. 
# This was developed off a script provided by Bryan Petersen from the VanLoocke Lab at Iowa State University. 
# For questions, email Leslie Stoecker, lensor@illinois.edu 

# Get the arguments passed through command line - ONLY uncomment if using it through a website
#syr, eyr, latN, latS, lonW, lonE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]

# Inputs to change
syr = 1979 # First year to pull data. The first year in the dataset is 1979
eyr = 2022 # Last year to pull data. There is current data, but it is not finalized currently.
latS = 25.06 # Southern boundary for the bounding box of interest. The southern border of the data is 25.06
latN = 49.4 # Northern boundary for the bounding box of interest. The northern border of the data is 49.4
lonW = -124.77 # Western boundary for the bounding box of interest. The western border of the data is -124.77
lonE = -67.06 # Eastern boundary for the bounding box of interest. The eastern border of the data is -67.06
dir = 'C:\\Users\\IGB\\Box\\Sustainability Hub\\GridMet Data Download\\' # Directory where all the files will be stored
delim = '\\' # Customizable file/directory delimiter depending on the system you are running it on


# Changes all the inputs to numbers
latN = float(latN)
latS = float(latS)
lonW = float(lonW)
lonE = float(lonE)
y=int(syr)

# Create folders if they do not exist
# First location to put the full data files
NWK_vars = ['tmmn','tmmx','pr','srad','vs','rmax','rmin']
for v in NWK_vars:
    var_dir = dir + v
    if not os.path.exists(var_dir):
        os.makedirs(var_dir)
        
# Location to put the AgroIBIS output data files
output_dir = dir + 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
OPT_vars = ['tmmn','tmax','prec','rads','wspd','high_relh','low_relh','ave_relh']
for v in OPT_vars:
    var_dir = output_dir + delim + v
    if not os.path.exists(var_dir):
        os.makedirs(var_dir)

# Loop through the years needed
while y<=int(eyr):
    
    # Minimum Air Temperature: Output will be tmmn_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/tmmn' + '_' + str(y) + '.nc'
    file = dir + 'tmmn' + delim + 'tmmn_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)
    temp = xr.open_dataset(file)
    temp = temp.rename({'day':'time'})
    temp = temp.rename({'air_temperature':'tmmn'})
    temp = temp.expand_dims('lev')
    temp = temp.assign_coords(lev = (temp.lev +1))
    temp = temp.tmmn - 273.15
    temp = temp.to_dataset()
    temp = temp.astype('double')
    temp.tmmn.attrs["units"] = "deg C"
    outfile = dir + 'Output' + delim + 'tmmn' + delim + 'tmmn_' + str(y) + '.nc'
    temp = temp.transpose("time","lev","lat","lon")
    cropped_temp = temp.sel(lat=slice(latN,latS), lon=slice(lonW,lonE))
    cropped_temp[['tmmn','time','lev','lat','lon']].to_netcdf(outfile,format = "NETCDF4_CLASSIC")
    xr.Dataset.close(temp)
    print('Finished: '  + str(y) + ' Minimum Temperature')
    
    # Maximum Air Temperature: Output will be tmax_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/tmmx' + '_' + str(y) + '.nc'
    file = dir + 'tmmx' + delim + 'tmmx_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)
    temp = xr.open_dataset(file)
    temp = temp.rename({'day':'time'})
    temp = temp.rename({'air_temperature':'tmax'})
    temp = temp.expand_dims('lev')
    temp = temp.assign_coords(lev = (temp.lev +1))
    temp = temp.tmax - 273.15
    temp = temp.to_dataset()
    temp = temp.astype('double')
    temp.tmax.attrs["units"] = "deg C"
    outfile = dir + 'Output' + delim + 'tmax' + delim + 'tmax_' + str(y) + '.nc'
    temp = temp.transpose("time","lev","lat","lon")
    cropped_temp = temp.sel(lat=slice(latN,latS), lon=slice(lonW,lonE))
    cropped_temp[['tmax','time','lev','lat','lon']].to_netcdf(outfile,format = "NETCDF4_CLASSIC")
    xr.Dataset.close(temp)
    print('Finished: ' + str(y) + ' Maximum Temperature')
    
    # Daily Precipitaiton Accumulation: Output will be prec_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/pr' + '_' + str(y) + '.nc'
    file = dir + 'pr' + delim + 'pr_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)
    temp = xr.open_dataset(file)
    temp = temp.rename({'day':'time'})
    temp = temp.rename({'precipitation_amount':'prec'})
    temp = temp.expand_dims('lev')
    temp = temp.assign_coords(lev = (temp.lev +1))
    temp = temp.drop(['crs'])
    temp = temp.astype('double')
    temp.prec.attrs["units"] = "mm"
    outfile = dir + 'Output' + delim + 'prec' + delim + 'prec_' + str(y) + '.nc'
    temp = temp.transpose("time","lev","lat","lon")
    cropped_temp = temp.sel(lat=slice(latN,latS), lon=slice(lonW,lonE))
    cropped_temp[['prec','time','lev','lat','lon']].to_netcdf(outfile,format = "NETCDF4_CLASSIC")
    xr.Dataset.close(temp)
    print('Finished: ' + str(y) + ' Precipitation')
    
    # Surface Downwelling Shortwave Radiation: Output will be rads_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/srad' + '_' + str(y) + '.nc'
    file = dir + 'srad' + delim + 'srad_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)
    temp = xr.open_dataset(file)
    temp = temp.rename({'day':'time'})
    temp = temp.rename({'surface_downwelling_shortwave_flux_in_air':'rads'})
    temp = temp.expand_dims('lev')
    temp = temp.assign_coords(lev = (temp.lev +1))
    temp = temp.drop(['crs'])
    temp = temp.astype('double')
    temp.rads.attrs["units"] = "W/m**2"
    outfile = dir + 'Output' + delim + 'rads' + delim + 'rads_' + str(y) + '.nc'
    temp = temp.transpose("time","lev","lat","lon")
    cropped_temp = temp.sel(lat=slice(latN,latS), lon=slice(lonW,lonE))
    cropped_temp[['rads','time','lev','lat','lon']].to_netcdf(outfile,format = "NETCDF4_CLASSIC")
    xr.Dataset.close(temp)
    print('Finished: ' + str(y) + ' Solar Radiation')
    
    # Wind Speed: Output will be wspd_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/vs' + '_' + str(y) + '.nc'
    file = dir + 'vs' + delim + 'vs_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)
    temp = xr.open_dataset(file)
    temp = temp.rename({'day':'time'})
    temp = temp.rename({'wind_speed':'wspd'})
    temp = temp.expand_dims('lev')
    temp = temp.assign_coords(lev = (temp.lev +1))
    temp = temp.drop(['crs'])
    temp = temp.astype('double')
    temp.wspd.attrs["units"] = "m/s"
    outfile = dir + 'Output' + delim + 'wspd' + delim + 'wspd_' + str(y) + '.nc'
    temp = temp.transpose("time","lev","lat","lon")
    cropped_temp = temp.sel(lat=slice(latN,latS), lon=slice(lonW,lonE))
    cropped_temp[['wspd','time','lev','lat','lon']].to_netcdf(outfile,format = "NETCDF4_CLASSIC")
    xr.Dataset.close(temp)
    print('Finished: ' + str(y) + ' Wind Speed')
    
    # Maximum Relative Humidity: Output will be relh_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/rmax' + '_' + str(y) + '.nc'
    file = dir + 'rmax' + delim + 'rmax_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)
    temp = xr.open_dataset(file)
    temp = temp.rename({'day':'time'})
    temp = temp.rename({'relative_humidity':'relh'})
    temp = temp.expand_dims('lev')
    temp = temp.assign_coords(lev = (temp.lev +1))
    temp = temp.drop(['crs'])
    temp = temp.astype('double')
    temp.relh.attrs["units"] = "percent"
    highrh_outfile = dir + 'Output' + delim + 'high_relh' + delim + 'relh_' + str(y) + '.nc'
    temp = temp.transpose("time","lev","lat","lon")
    cropped_temp = temp.sel(lat=slice(latN,latS), lon=slice(lonW,lonE))
    cropped_temp[['relh','time','lev','lat','lon']].to_netcdf(highrh_outfile,format = "NETCDF4_CLASSIC")
    xr.Dataset.close(temp)
    print('Finished: '  + str(y) + ' Maximum Relative Humidity')
    
    # Minimum Relative Humidity: Output will be relh_yyyy.nc
    url = 'http://www.northwestknowledge.net/metdata/data/rmin_' + str(y) + '.nc'
    file = dir + 'rmin' + delim + 'rmin_' + str(y) + '.nc'
    if not os.path.exists(file):
        f = wget.download(url, out=file)
    temp = xr.open_dataset(file)
    temp = temp.rename({'day':'time'})
    temp = temp.rename({'relative_humidity':'relh'})
    temp = temp.expand_dims('lev')
    temp = temp.assign_coords(lev = (temp.lev +1))
    temp = temp.drop(['crs'])
    temp = temp.astype('double')
    temp.relh.attrs["units"] = "percent"
    lowrh_outfile = dir + 'Output' + delim + 'low_relh' + delim + 'relh_' + str(y) + '.nc'
    temp = temp.transpose("time","lev","lat","lon")
    cropped_temp = temp.sel(lat=slice(latN,latS), lon=slice(lonW,lonE))
    cropped_temp[['relh','time','lev','lat','lon']].to_netcdf(lowrh_outfile,format = "NETCDF4_CLASSIC")
    xr.Dataset.close(temp)
    print('Finished: '  + str(y) + ' Minimum Relative Humidity')
    
    
    #Average Relative Humidity: Output is relh_yyyy.nc
    low_rh = xr.open_dataset(lowrh_outfile)
    high_rh = xr.open_dataset(highrh_outfile)
    
    rh_ave = (low_rh['relh']+high_rh['relh'])/2
    rh_ave = rh_ave.to_dataset()
    rh_ave = rh_ave.astype('double')
    rh_ave.relh.attrs['units'] = 'percent'
    rh_ave = rh_ave.transpose('time','lev','lat','lon')
    rh_ave[['relh','time','lev','lat','lon']].to_netcdf(dir + 'Output' + delim + 'ave_relh' + delim + 'relh_' + str(y) + '.nc')
    xr.Dataset.close(rh_ave)
    xr.Dataset.close(low_rh)
    xr.Dataset.close(high_rh)
    print('Finished: ' + str(y) + ' Average Relative Humidity')

    
    y = y+1
