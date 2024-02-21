## GRIDMet
#### Description
GRIDMET is a dataset of daily high-spatial resolution (~4-km, 1/24th degree) surface meteorological data covering the contiguous US from 1979-yesterday. We have also extended these data to cover southern British Columbia in our real time products. These data can provide important inputs for ecological, agricultural, and hydrological models. These data are updated daily.  gridMET is the preferred naming convention for these data; however, the data are also known as cited as METDATA.

**Primary Climate Variables**
* Temperature - maximum and minimum
* Precipitation accumulation
* Downward surface shortwave radiation
* Wind velocity
* Humidity - maximum and minimum relative humidity and specific humidity

**Derived Variables**
* Reference evapotranspiration
* Energy Release Component
* Burning Index
* 100-hour and 1000-hour dead fuel moisture
* Mean vapor pressure deficit
* 10-day Palmer Drought Severity Index

The files are in netCDF format

*More information can be found from the Climatology Lab's Website, [https://www.climatologylab.org/gridmet.html]* 
#### Access

Direct file downloads:
1. [Direct download of NetCDF files](https://www.northwestknowledge.net/metdata/data/)
2. Create [wget script](https://www.climatologylab.org/wget-gridmet.html) for downloading NetCDF files
3. [THREDDS Catalog (OPENDAP)](http://thredds.northwestknowledge.net:8080/thredds/reacch_climate_MET_catalog.html))
4. [Aggregated THREDDS Catalog (OPENDAP)](http://thredds.northwestknowledge.net:8080/thredds/reacch_climate_MET_aggregated_catalog.html)
5. [Elevation data](https://climate.northwestknowledge.net/METDATA/data/metdata_elevationdata.nc) on the same 4-km grid as the Meteorological data.

Data subsets can be accessed using the web tools:
1. [ClimateEngine.org](https://app.climateengine.org/)
2. [Geo Data Portal](https://cida.usgs.gov/gdp/client/#!catalog/gdp/dataset/54dd5df2e4b08de9379b38d8)

#### Scripts

##### Convert_Gridmet_Daily_Data_to_IBIS.py
This is a python script created by Bryan Peterson from the VanLoocke Lab at Iowa State to convert the netCDF files for use into AgroIBIS. 

**Modules Required**
* numpy
* pandas
* xarray
* xesmf
* netCDF4
* os
* glob

**Data**
You will need to download the GridMet data required and place it in a directory that the script can access.

The folder structure in the script organizes the data by variable:
* tmmn: Minimum Temperature
* tmax: Maximum Temperature
* prec: Precipitation
* rads: Downward Surface Shortwave Radiation
* relh: Maximum Relative Humidity
* wspd: Wind Speed
* low_relh: Minimum Relative Humidity
