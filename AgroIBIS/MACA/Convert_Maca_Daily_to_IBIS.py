#!/usr/bin/env python
# coding: utf-8

# This program will open MACAv2-METDATA datasets from their directory and convert the dataset into a usable version for Agro-IBIS. It will output the new netcdfs to designated directories. Written by Madelynn Wuestenberg.
# The input is the files downloaded from the MACA website sitting on the server. It opens each year and pulls out the correct geographical area for the AgroIBIS. Each meteorological element is written out into a new netcdf file. Also, it calculates the daily relative humidity and the uv wind, which are also output.


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
import datetime as dt


# This is set up for historical tmin
for dirname in ["historical"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_tmin/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 1950
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_tmin/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        #temp = temp.rename({'day':'time'})
        temp = temp.rename({'air_temperature':'tmin'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        temp = temp.tmin - 273.15
     
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
    
        temp = temp.to_dataset()
        file_2 = f"/Volumes/Madelynn_Raid/maca/tmin/{dirname}/tmin_%s.nc" % year # Need to change to the location of where to write
        temp.tmin.attrs["units"] = "deg C"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['tmin','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")

        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir("..")


# This is for future scenarios, RCP4.5 and RCP8.5, for tmin

for dirname in ["rcp45", "rcp85"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_tmin/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 2006
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_tmin/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        #temp = temp.rename({'day':'time'})
        temp = temp.rename({'air_temperature':'tmin'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        temp = temp.tmin - 273.15
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
        temp = temp.to_dataset()
        file_2 = f"/Volumes/Madelynn_Raid/maca/tmin/{dirname}/tmin_%s.nc" % year # Need to change to the location of where to write
        temp.tmin.attrs["units"] = "deg C"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['tmin','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir("..")

# This is set up for historical tmax
for dirname in ["historical"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_tmax/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 1950
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_tmax/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'air_temperature':'tmax'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        temp = temp.tmax - 273.15
    
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
        temp = temp.to_dataset()
        temp.tmax.attrs["units"] = "deg C"
        file_2 = f"/Volumes/Madelynn_Raid/maca/tmax/{dirname}/tmax_%s.nc" % year # Need to change to the location of where to write
        temp = temp.transpose("time","lev","lat","lon")
        temp[['tmax','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir("..")

# This is for future scenarios, RCP4.5 and RCP8.5, for tmax

for dirname in ["rcp45", "rcp85"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_tmax/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 2006
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_tmax/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'air_temperature':'tmax'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        temp = temp.tmax - 273.15
    
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
    
        temp = temp.to_dataset()
        temp.tmax.attrs["units"] = "deg C"
        file_2 = f"/Volumes/Madelynn_Raid/maca/tmax/{dirname}/tmax_%s.nc" % year # Need to change to the location of where to write
        temp = temp.transpose("time","lev","lat","lon")
        temp[['tmax','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir("..")

# This is set up for historical precipitation
for dirname in ["historical"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_precip/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 1950
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_precip/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'precipitation':'prec'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
    
        #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        #temp = temp.to_dataset()
        temp.prec.attrs["units"] = "mm"
        file_2 = f"/Volumes/Madelynn_Raid/maca/prec/{dirname}/prec_%s.nc" % year # Need to change to the location of where to write
        temp = temp.transpose("time","lev","lat","lon")
        temp[['prec','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir("..")

# This is for future scenarios, RCP4.5 and RCP8.5, for precipitation
for dirname in ["rcp45", "rcp85"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_precip/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 2006
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_precip/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'precipitation':'prec'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
        #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        #temp = temp.to_dataset()
        temp.prec.attrs["units"] = "mm"
        file_2 = f"/Volumes/Madelynn_Raid/maca/prec/{dirname}/prec_%s.nc" % year # Need to change to the location of where to write
        temp = temp.transpose("time","lev","lat","lon")
        temp[['prec','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir("..")

# This is set up for historical solar radiation
for dirname in ["historical"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_solrad/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 1950
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_solrad/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'surface_downwelling_shortwave_flux_in_air':'rads'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
        
        #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/rads/{dirname}/rads_%s.nc" % year # Need to change to the location of where to write
        temp.rads.attrs["units"] = "W/m**2"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['rads','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir("..")

# This is for future scenarios, RCP4.5 and RCP8.5, for solar radiation
for dirname in ["rcp45", "rcp85"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_solrad/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 2006
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_solrad/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'surface_downwelling_shortwave_flux_in_air':'rads'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
        
        #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/rads/{dirname}/rads_%s.nc" % year # Need to change to the location of where to write
        temp.rads.attrs["units"] = "W/m**2"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['rads','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir("..")

# This is set up for historical maximum relative humidity
for dirname in ["historical"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_rhmax/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 1950
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_rhmax/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'relative_humidity':'relh'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
        
        
     #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/high_relh/{dirname}/relh_%s.nc" % year # Need to change to the location of where to write
        temp.relh.attrs["units"] = "percent"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir('..')

# This is for future scenarios, RCP4.5 and RCP8.5, for maximum relative humidity
for dirname in ["rcp45", "rcp85"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_rhmax/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 2006
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_rhmax/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'relative_humidity':'relh'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
     #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/high_relh/{dirname}/relh_%s.nc" % year # Need to change to the location of where to write
        temp.relh.attrs["units"] = "percent"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir('..')

# This is set up for historical minimum relative humidity
for dirname in ["historical"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_rhmin/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 1950
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_rhmin/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'relative_humidity':'relh'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
     #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/low_relh/{dirname}/relh_%s.nc" % year # Need to change to the location of where to write
        temp.relh.attrs["units"] = "percent"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir('..')

# This is for future scenarios, RCP4.5 and RCP8.5, for minimum relative humidity
for dirname in ["rcp45", "rcp85"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_rhmin/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 2006
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_rhmin/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
        temp = temp.rename({'relative_humidity':'relh'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
     #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/low_relh/{dirname}/relh_%s.nc" % year # Need to change to the location of where to write
        temp.relh.attrs["units"] = "percent"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir('..')

# Calculate the mean rh from the high and low datasets
for yr in range(1950,2006):   

 low_rh = xr.open_dataset(f"/Volumes/Madelynn_Raid/maca/low_relh/historical/relh_{yr}.nc") # Need to change to the location of where the files written above are
 high_rh = xr.open_dataset(f"/Volumes/Madelynn_Raid/maca/high_relh/historical/relh_{yr}.nc") # Need to change to the location of where the files written above are

 rh_ave = (low_rh['relh']+high_rh['relh'])/2
 rh_ave = rh_ave.to_dataset()
 rh_ave = rh_ave.astype('double')
 rh_ave.relh.attrs["units"] = "percent"
 rh_ave = rh_ave.transpose("time","lev","lat","lon")
 file_2 = f"/Volumes/Madelynn_Raid/maca/ave_rh/historical/relh_{yr}.nc" # Need to change to the location of where to write
 rh_ave[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 xr.Dataset.close(rh_ave)
 xr.Dataset.close(low_rh)
 xr.Dataset.close(high_rh)

# Calculate the mean rh for the RCP4.5 dataset
for yr in range(2006,2100):   

 low_rh = xr.open_dataset(f"/Volumes/Madelynn_Raid/maca/low_relh/rcp45/relh_{yr}.nc") # Need to change to the location of where the files written above are
 high_rh = xr.open_dataset(f"/Volumes/Madelynn_Raid/maca/high_relh/rcp45/relh_{yr}.nc") # Need to change to the location of where the files written above are

 rh_ave = (low_rh['relh']+high_rh['relh'])/2
 rh_ave = rh_ave.to_dataset()
 rh_ave = rh_ave.astype('double')
 rh_ave.relh.attrs["units"] = "percent"
 rh_ave = rh_ave.transpose("time","lev","lat","lon")
 file_2 = f"/Volumes/Madelynn_Raid/maca/ave_rh/rcp45/relh_{yr}.nc" # Need to change to the location of where to write
 rh_ave[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 xr.Dataset.close(rh_ave)
 xr.Dataset.close(low_rh)
 xr.Dataset.close(high_rh)

# Calculate the mean rh for the RCP8.5 dataset
for yr in range(2006,2100):   

 low_rh = xr.open_dataset(f"/Volumes/Madelynn_Raid/maca/low_relh/rcp85/relh_{yr}.nc") # Need to change to the location of where the files written above are
 high_rh = xr.open_dataset(f"/Volumes/Madelynn_Raid/maca/high_relh/rcp85/relh_{yr}.nc") # Need to change to the location of where the files written above are

 rh_ave = (low_rh['relh']+high_rh['relh'])/2
 rh_ave = rh_ave.to_dataset()
 rh_ave = rh_ave.astype('double')
 rh_ave.relh.attrs["units"] = "percent"
 rh_ave = rh_ave.transpose("time","lev","lat","lon")
 file_2 = f"/Volumes/Madelynn_Raid/maca/ave_rh/rcp85/relh_{yr}.nc" # Need to change to the location of where to write
 rh_ave[['relh','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
 xr.Dataset.close(rh_ave)
 xr.Dataset.close(low_rh)
 xr.Dataset.close(high_rh)

# This is set up for historical eastward wind
for dirname in ["historical"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_u/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 1950
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_u/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
    # temp = temp.rename({'day':'time'})
        temp = temp.rename({'eastward_wind':'wspd'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
     #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/u/historical/u_%s.nc" % year # Need to change to the location of where to write
        temp.wspd.attrs["units"] = "m/s"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['wspd','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir('..')

# This is for future scenarios, RCP4.5 and RCP8.5, for eastward wind
for dirname in ["rcp45", "rcp85"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_u/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 2006
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_u/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
    # temp = temp.rename({'day':'time'})
        temp = temp.rename({'eastward_wind':'wspd'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
     #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/u/{dirname}/u_%s.nc" % year # Need to change to the location of where to write
        temp.wspd.attrs["units"] = "m/s"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['wspd','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir('..')

# This is set up for historical northward wind
for dirname in ["historical"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_v/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 1950
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_v/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
    # temp = temp.rename({'day':'time'})
        temp = temp.rename({'northward_wind':'wspd'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
     #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/v/historical/v_%s.nc" % year # Need to change to the location of where to write
        temp.wspd.attrs["units"] = "m/s"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['wspd','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir('..')

# This is for future scenarios, RCP4.5 and RCP8.5, for northward wind
for dirname in ["rcp45", "rcp85"]:
    path = f'/Volumes/Madelynn_Raid/maca_testdata/new1_v/{dirname}' # Need to change to the location of the MACA files
    os.chdir(path)
    year = 2006
    for filename in glob.glob(f"/Volumes/Madelynn_Raid/maca_testdata/new1_v/{dirname}/*.nc"): # Need to change to the location of the MACA files
        temp = xr.open_dataset(filename)
    # temp = temp.rename({'day':'time'})
        temp = temp.rename({'northward_wind':'wspd'})
        temp = temp.expand_dims("lev")
        temp = temp.assign_coords(lev = (temp.lev +1))
        
        lon_name = 'lon'  # whatever name is in the data

        # Adjust lon values to make sure they are within (-180, 180)
        temp['_longitude_adjusted'] = xr.where(
            temp[lon_name] > 180,
            temp[lon_name] - 360,
            temp[lon_name])

        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
        temp = (
            temp
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(temp._longitude_adjusted)})
            .drop(lon_name))

        temp = temp.rename({'_longitude_adjusted': lon_name})
     #temp = temp.drop(['crs'])
        temp = temp.astype('double')
        file_2 = f"/Volumes/Madelynn_Raid/maca/v/{dirname}/v_%s.nc" % year # Need to change to the location of where to write
        temp.wspd.attrs["units"] = "m/s"
        temp = temp.transpose("time","lev","lat","lon")
        temp[['wspd','time','lev','lat','lon']].to_netcdf(file_2,format = "NETCDF4_CLASSIC")
        year = year+1
        xr.Dataset.close(temp)
        temp.close()
    os.chdir('..')
  
# Combine the historical u and v wind into one wind speed
for year in range(1950,2006):
    u = xr.open_dataset('/Volumes/Madelynn_Raid/maca/u/historical/u_%s.nc' % year) # Need to change to the location of where the files written above are
    #print(u)
    #u = u.rename({'eastward_wind':'wspd'})
    v = xr.open_mfdataset('/Volumes/Madelynn_Raid/maca/v/historical/v_%s.nc' % year) # Need to change to the location of where the files written above are
    #v = v.rename({'northward_wind':'wspd'})
    u['wspd'] = wind_uv_to_spd(u.wspd,v.wspd)
    file_2 = f"/Volumes/Madelynn_Raid/maca/wspd/historical/wspd_{year}.nc" # Need to change to the location of where to write
    u.to_netcdf(file_2, format = "NETCDF4_CLASSIC")
    u.close()
    v.close()

# Combine the future RCP4.5 u and v wind into one wind speed
for year in range(2006,2100):
    u = xr.open_dataset('/Volumes/Madelynn_Raid/maca/u/rcp45/u_%s.nc' % year) # Need to change to the location of where the files written above are
    #print(u)
    #u = u.rename({'eastward_wind':'wspd'})
    v = xr.open_mfdataset('/Volumes/Madelynn_Raid/maca/v/rcp45/v_%s.nc' % year) # Need to change to the location of where the files written above are
    #v = v.rename({'northward_wind':'wspd'})
    u['wspd'] = wind_uv_to_spd(u.wspd,v.wspd)
    file_2 = f"/Volumes/Madelynn_Raid/maca/wspd/rcp45/wspd_{year}.nc" # Need to change to the location of where to write
    u.to_netcdf(file_2, format = "NETCDF4_CLASSIC")
    u.close()
    v.close()

# Combine the future RCP8.5 u and v wind into one wind speed
for year in range(2006,2100):
    u = xr.open_dataset('/Volumes/Madelynn_Raid/maca/u/rcp85/u_%s.nc' % year) # Need to change to the location of where the files written above are
    #print(u)
    #u = u.rename({'eastward_wind':'wspd'})
    v = xr.open_mfdataset('/Volumes/Madelynn_Raid/maca/v/rcp85/v_%s.nc' % year) # Need to change to the location of where the files written above are
    #v = v.rename({'northward_wind':'wspd'})
    u['wspd'] = wind_uv_to_spd(u.wspd,v.wspd)
    file_2 = f"/Volumes/Madelynn_Raid/maca/wspd/rcp85/wspd_{year}.nc" # Need to change to the location of where to write
    u.to_netcdf(file_2, format = "NETCDF4_CLASSIC")
    u.close()
    v.close()
