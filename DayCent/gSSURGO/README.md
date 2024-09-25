## gSSURGO
### Description
The Gridded Soil Survey Geographic Database is similar to SSURGO but in the format of an ESRI file geodatabase. The tabular data represent the soil attributes and are derived from properties and characteristics stored in the National Soil Information System (NASIS). 

*More information about the gSSURGO Database can be found from the NRCS website, https://www.nrcs.usda.gov/resources/data-and-reports/gridded-soil-survey-geographic-gssurgo-database*

### Scripts

#### get_DayCent_soilsin_files_for_longlats.R

This is an R script provided by Jeff Kent formerly from the Hudiburg Lab at the University of Idaho. This script allows users to input a list of latitude/longitude points and determine what gSSURGO area to use.

**Library Required**
* soilDB

**How to Use**

1. Ensure you have the soilDB library installed
2. Download the [R-script](https://github.com/cabbi-bio/Sustainability-Shared-Code/blob/main/DayCent/gSSURGO/getDayCent_soilsin_files_for_longlats.R)
3. On lines 9 and 10, delete NA and replace with a list of the latitudes (line 9) and longitudes (line 10) for which you need locations. Multiple entries can be used for one run of the script.
4. Then run the script using R.
5. The sites are located in a file called simsites_SSURGO_soilsin.tsv.
