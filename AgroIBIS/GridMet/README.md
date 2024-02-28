## GRIDMet
### Description
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
### Access

Direct file downloads:
1. [Direct download of NetCDF files](https://www.northwestknowledge.net/metdata/data/)
2. Create [wget script](https://www.climatologylab.org/wget-gridmet.html) for downloading NetCDF files
3. [THREDDS Catalog (OPENDAP)](http://thredds.northwestknowledge.net:8080/thredds/reacch_climate_MET_catalog.html))
4. [Aggregated THREDDS Catalog (OPENDAP)](http://thredds.northwestknowledge.net:8080/thredds/reacch_climate_MET_aggregated_catalog.html)
5. [Elevation data](https://climate.northwestknowledge.net/METDATA/data/metdata_elevationdata.nc) on the same 4-km grid as the Meteorological data.

Data subsets can be accessed using the web tools:
1. [ClimateEngine.org](https://app.climateengine.org/)
2. [Geo Data Portal](https://cida.usgs.gov/gdp/client/#!catalog/gdp/dataset/54dd5df2e4b08de9379b38d8)

*For data formatted for AgroIBIS see the gridMetAgroIBIS.py script below*

### Scripts

#### gridMetAgroIBIS.py

This is a Python 3 script modified from a script provided by [Bryan Peterson](bryan20@iastate.edu) from the VanLoocke Lab at Iowa State to download the GridMet data required to run AgroIBIS. It downloads the data from the 
[University of Idaho](https://www.northwestknowledge.net/metdata/data/). It allows users to customize what years they want to download and also the spatial dimension of interest (a bounding box with a North/South latitude and West/East latitude). For questions regarding this script, contact [Leslie Stoecker](lensor@illinois.edu).

**Modules Required**
* os
* sys
* wget
* xarray
* netCDF4

**How to Use**

1. Ensure all the needed modules are downloaded. [Anaconda](https://www.anaconda.com/download) or [PIP](https://packaging.python.org/en/latest/tutorials/installing-packages/) are good tools to use for this.
2. Download the [gridMetAgroIBIS.py](https://github.com/cabbi-bio/Sustainability-Shared-Code/blob/main/AgroIBIS/GridMet/gridMetAgroIBIS.py) script
3. Open the script and find the "Inputs to change" section
4. Change syr to the first year you need
5. Change eyr to the last year you need
6. Change latN, latS, lonW, lonE to the bounding box needed. All should be in decimal degrees. Latitude is in decimal degrees north and longitude is in decimal degrees east
7. Change dir to the directory where you want to download the data
8. Change delim to the slash needed for your system. If you're running this on Linux, you'll likely want to use '/', and if you're using Windows, it will likely be '\\'.
9. The script will create other directories that are needed
10. Only minimum temperature, maximum temperature, solar radiation, preciptiation, wind speed, minimum relative humidity and maximum relative humidity files are downloaded and processed. Average daily relative humidity will be calculated as well.
11. The full downloaded files will be stored in the directory. After the script runs, you can delete them.
12. The processed files will be in a directory called 'Output'.
