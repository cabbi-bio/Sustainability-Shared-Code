#!/usr/bin/env python
# coding: utf-8

# Script provided by Bryan Petersen, bryan20@iastate.edu, VanLoocke Lab, Iowa State University. 
# Converts the GridMet daily data into a netcdf for use in AgroIBIS. 

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.units import units
import numpy as np
import pandas as pd
import xarray as xr
import xesmf
import netCDF4
import os
import glob

# Opens the minimum temperature files for all the years. Converts the file to the format needed for AgroIBIS and units to Celsius
year = 1990
for filename in glob.glob("/Volumes/lab_ssd/tmmn/*.nc"): # Location needs to be changed
 temp = xr.open_dataset(filename)
 temp = temp.rename({'day':'time'})
 temp = temp.rename({'air_temperature':'tmmn'})
 temp = temp.expand_dims("lev")
 temp = temp.assign_coords(lev = (temp.lev +1))
 temp = temp.tmin - 273.15
 temp = temp.to_dataset()
 temp = temp.astype('double')
 file_2 = "/Volumes/lab_ssd/new_tmmn/tmmn_%s.nc" % year # Location of saved files will need to be changed
 temp.tmin.attrs["units"] = "deg C"
 temp = temp.transpose("time","lev","lat","lon")
 temp[['tmmn','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 year = year+1
 xr.Dataset.close(temp)

# Opens the maximum temperature files for all the years. Converts the file to the format needed for AgroIBIS and units to Celsius
year = 1990
for filename in glob.glob("/Volumes/lab_ssd/tmax/*.nc"): # Location needs to be changed
 temp = xr.open_dataset(filename)
 temp = temp.rename({'day':'time'})
 temp = temp.rename({'air_temperature':'tmax'})
 temp = temp.expand_dims("lev")
 temp = temp.assign_coords(lev = (temp.lev +1))
 temp = temp.tmax - 273.15
 temp = temp.to_dataset()
 temp = temp.astype('double')
 file_2 = "/Volumes/lab_ssd/new_tmax/tmax_%s.nc" % year # Location of saved files will need to be changed
 temp.tmax.attrs["units"] = "deg C"
 temp = temp.transpose("time","lev","lat","lon")
 temp[['tmax','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 year = year+1
 xr.Dataset.close(temp)

# Opens the precipitation files for all the years. Converts the file to the format needed for AgroIBIS.
year = 1990
for filename in glob.glob("/Volumes/lab_ssd/prec/*.nc"): # Location needs to be changed
 temp = xr.open_dataset(filename)
 temp = temp.rename({'day':'time'})
 temp = temp.rename({'precipitation_amount':'prec'})
 temp = temp.expand_dims("lev")
 temp = temp.assign_coords(lev = (temp.lev +1))
 temp = temp.drop(['crs'])
 temp = temp.astype('double')
 #temp = temp.to_dataset()
 file_2 = "/Volumes/lab_ssd/new_prec/prec_%s.nc" % year # Location of saved files will need to be changed
 temp.prec.attrs["units"] = "mm"
 temp = temp.transpose("time","lev","lat","lon")
 temp[['prec','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 year = year+1
 xr.Dataset.close(temp)

# Opens the solar radiation files for all the years. Converts the file to the format needed for AgroIBIS
year = 1990
for filename in glob.glob("/Volumes/lab_ssd/rads/*.nc"): # Location needs to be changed
 temp = xr.open_dataset(filename)
 temp = temp.rename({'day':'time'})
 temp = temp.rename({'surface_downwelling_shortwave_flux_in_air':'rads'})
 temp = temp.expand_dims("lev")
 temp = temp.assign_coords(lev = (temp.lev +1))
 temp = temp.drop(['crs'])
 temp = temp.astype('double')
 file_2 = "/Volumes/lab_ssd/new_rads/rads_%s.nc" % year # Location of saved files will need to be changed
 temp.rads.attrs["units"] = "W/m**2"
 temp = temp.transpose("time","lev","lat","lon")
 temp[['rads','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 year = year+1
 xr.Dataset.close(temp)

# Opens the maximum relative humidity files for all the years. Converts the file to the format needed for AgroIBIS
year = 1990
for filename in glob.glob("/Volumes/lab_ssd/relh/*.nc"): # Location needs to be changed
 temp = xr.open_dataset(filename)
 temp = temp.rename({'day':'time'})
 temp = temp.rename({'relative_humidity':'relh'})
 temp = temp.expand_dims("lev")
 temp = temp.assign_coords(lev = (temp.lev +1))
 temp = temp.drop(['crs'])
 temp = temp.astype('double')
 file_2 = "/Volumes/lab_ssd/new_high_relh/relh_%s.nc" % year # Location of saved files will need to be changed.
 temp.relh.attrs["units"] = "percent"
 temp = temp.transpose("time","lev","lat","lon")
 temp[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 year = year+1
 xr.Dataset.close(temp)

# Opens the wind speed files for all the years. Converts the file to the format needed for AgroIBIS
year = 1990
for filename in glob.glob("/Volumes/lab_ssd/wspd/*.nc"): # Location needs to be changed
 temp = xr.open_dataset(filename)
 temp = temp.rename({'day':'time'})
 temp = temp.rename({'wind_speed':'wspd'})
 temp = temp.expand_dims("lev")
 temp = temp.assign_coords(lev = (temp.lev +1))
 temp = temp.drop(['crs'])
 temp = temp.astype('double')
 file_2 = "/Volumes/lab_ssd/new_wspd/wspd_%s.nc" % year # Location of saved files will need to be changed.
 temp.wspd.attrs["units"] = "m/s"
 temp = temp.transpose("time","lev","lat","lon")
 temp[['wspd','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 year = year+1
 xr.Dataset.close(temp)

# Opens the minimum relative humidity files for all the years. Converts the file to the format needed for AgroIBIS
year = 1990
for filename in glob.glob("/Volumes/lab_ssd/low_relh/*.nc"): # Location needs to be changed
 temp = xr.open_dataset(filename)
 temp = temp.rename({'day':'time'})
 temp = temp.rename({'relative_humidity':'relh'})
 temp = temp.expand_dims("lev")
 temp = temp.assign_coords(lev = (temp.lev +1))
 temp = temp.drop(['crs'])
 temp = temp.astype('double')
 file_2 = "/Volumes/lab_ssd/new_low_relh/relh_%s.nc" % year # Location of saved files will need to be changed.
 temp.relh.attrs["units"] = "percent"
 temp = temp.transpose("time","lev","lat","lon")
 temp[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 year = year+1
 xr.Dataset.close(temp)

# This section takes the minimum and maximum relative humidity and creates the average daily relative humidity
low_rh = xr.open_dataset(f"/Volumes/lab_ssd/new_low_relh/relh_1990.nc") # Location needs to be changed
high_rh = xr.open_dataset(f"/Volumes/lab_ssd/new_high_relh/relh_1990.nc") # Location needs to be changed

rh_ave = (low_rh['relh']+high_rh['relh'])/2
rh_ave = rh_ave.to_dataset()
rh_ave = rh_ave.astype('double')
rh_ave.relh.attrs["units"] = "percent"
rh_ave = rh_ave.transpose("time","lev","lat","lon")
rh_ave[['relh','time','lev','lat','lon']].to_netcdf(f"/Volumes/lab_ssd/new_ave_relh/relh_1990.nc",format = "NETCDF4_CLASSIC") # Location of saved files will need to be changed.
xr.Dataset.close(rh_ave)
xr.Dataset.close(low_rh)
xr.Dataset.close(high_rh)
