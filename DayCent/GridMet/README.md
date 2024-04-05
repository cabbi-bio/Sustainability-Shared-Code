## GRIDMET
### Description
GRIDMET is a dataset of daily high-spatial resolution (~4-km, 1/24th degree) surface meteorological data covering the contiguous US from 1979-yesterday. These data can provide important inputs for ecological, agricultural, and hydrological models. These data are updated daily. 

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

*More information can be found from the Climatology Lab's Website, https://www.climatologylab.org/gridmet.html* 
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

*For data formatted for DayCent, see the scripts below*

### Scripts

#### gridDayCent.py

This is a Python 3 script provided by [Theo Hartman](tmihart@illinois.edu) from the Heaton Lab at Illinois to download the GridMet data required to run DayCent. It downloads the data from the 
[University of Idaho](https://www.northwestknowledge.net/metdata/data/). This script allows users to customize what years of interest to extract data for the nearest gridpoint to a specific latitude/longitude coordinate. 
For questions regarding this script, contact [Leslie Stoecker](lensor@illinois.edu).

**Modules Required**
* os
* sys
* wget
* xarray
* netCDF4
* numpy
* pandas

**How to Use**

1. Ensure all the needed modules are downloaded. [Anaconda](https://www.anaconda.com/download) or [PIP](https://packaging.python.org/en/latest/tutorials/installing-packages/) are good tools to use for this.
2. Download the [gridMetDayCent.py](https://github.com/cabbi-bio/Sustainability-Shared-Code/blob/main/DayCent/GridMet/gridMetDayCent.py) script
3. If you have a list of locations (lat/lon coordinates) to download see [gridMetDayCentFileInput.py](#gridMetDayCentFileInputpy) below. Otherwise continue with remaining steps.
4. Comment out (using a #) on line 16, and uncomment out lines 19-25 (remove the # at the start of the line)
5. Change syr to the first year you need
6. Change eyr to the last year you need
7. Change latitude and longitude to the points of interest. Latitude is in decimal degrees north and longitude is in decimal degrees east
8. Change dir to the directory where you want to download the data
9. Change delim to the slash needed for your system. If you're running this on Linux, you'll likely want to use '/', and if you're using Windows, it will likely be '\\'.
10. The script will create other directories that are needed
11. Only minimum temperature, maximum temperature, solar radiation, preciptiation, wind speed, minimum relative humidity and maximum relative humidity files are downloaded and processed. Average daily relative humidity will be calculated as well.
12. The full downloaded files will be stored in the directory. After the script runs, you can delete them.
13. The processed files will be in the original directory that you specified.

#### gridMetDayCentFileInput.py

This is a Python 3 script that is a wrapper for [gridDayCent.py](#gridDayCentpy). It takes a comma-delimited file of location names, latitudes and longitudes and processes GridMet data for each one and for the years specified. 
For questions regarding this script, contact [Leslie Stoecker](lensor@illinois.edu).

**Modules Required**
* os
* sys
* numpy
* subprocess

**How to Use**

1. Ensure all the needed modules for this script and for [gridDayCent.py](#gridDayCentpy) are installed. [Anaconda](https://www.anaconda.com/download) or [PIP](https://packaging.python.org/en/latest/tutorials/installing-packages/) are good tools to use for this.
2. Download the [gridMetDayCent.py](https://github.com/cabbi-bio/Sustainability-Shared-Code/blob/main/DayCent/GridMet/gridMetDayCent.py) and the script [gridMetDayCentFileInput.py](https://github.com/cabbi-bio/Sustainability-Shared-Code/blob/main/DayCent/GridMet/gridMetDayCentFileInput.py)
3. Open gridMetDayCentFileInput.py and go to the Inputs to change section
4. Change syr to the first year you need
5. Change eyr to the last year you need
6. Change dir to the directory where you want to download the data
7. Change delim to the slash needed for your system. If you're running this on Linux, you'll likely want to use '/', and if you're using Windows, it will likely be '\\'.
8. Change filename to the name of your file that has the list of location names, latitudes and longitudes. See the example file in this directory.
9. Only minimum temperature, maximum temperature, solar radiation, preciptiation, wind speed, minimum relative humidity and maximum relative humidity files are downloaded and processed. Average daily relative humidity will be calculated as well.
10. The full downloaded files will be stored in the directory. After the script runs, you can delete them.
11. The formated text files will be in the original directory that you specified.
