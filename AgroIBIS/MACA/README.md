## MACA
### Description
MACA (Multivariate Adaptive Constructed Analogs) is a statistical method for downscaling Global Climate Models (GCMs) from their native coarse resolution to a higher spatial resolution that captures reflects observed 
patterns of daily near-surface meteorology and simulated changes in GCMs experiments. This method has been shown to be slightly preferable to direct daily interpolated bias correction in regions of complex terrain due to 
its use of a historical library of observations and multivariate approach.

Two different downscaled data covering CONUS-plus using a common set of 20 CMIP5 GCMs form modesl that provided daily output of requisite variables form historical (1950-2005) and future experiements under RCP4.5 and $CP8.5. 

**Climate Variables**
* Temperature - maximum and minimum
* Precipitation accumulation
* Downward surface shortwave radiation
* Wind velocity
* Humidity - maximum and minimum relative humidity and specific humidity

For these scripts, the files are in netCDF format

*More information can be found from the Climatology Lab's Website, [https://www.climatologylab.org/maca.html](https://www.climatologylab.org/maca.html)* 
### Access

Direct file downloads:
1. [Catalog of netCDF files for MACA housed at the Northwest Knowledge Network](http://climate.northwestknowledge.net/MACA/data_catalogs.php)
2. Also there are multiple dataservices where it can be accessed through OPENDAP, THREDDS or other methods. See the Climate Lab's website above.

Data subsets can be accessed using the web tools:
1. [Download gridded data for specific region(s) as netCDF files](https://climate.northwestknowledge.net/MACA/data_portal.php)

### Scripts

**Convert_Gridmet_Daily_Data_to_IBIS.py**

This is a python script provided by Madelynn Wuestenberg from the [VanLoocke Lab](andyvanl@iastate.edu) at Iowa State to convert the netCDF files for use into AgroIBIS. 

**Modules Required**
* numpy
* pandas
* xarray
* xesmf
* netCDF4
* os
* glob
* metpy

**Data**
You will need to download the MACA data that you are interested in using (specific models, variables) and place it in a directory that the script can access.

The folder structure in the script organizes the data by variable:
* tmmn: Minimum Temperature
* tmax: Maximum Temperature
* prec: Precipitation
* rads: Downward Surface Shortwave Radiation
* relh: Maximum Relative Humidity
* wspd: Wind Speed
* low_relh: Minimum Relative Humidity
