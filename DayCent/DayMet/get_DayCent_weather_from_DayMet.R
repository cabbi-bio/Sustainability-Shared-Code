## this script needs to run within an R session and needs the "lubridate" package for converting between file types
# mysitecoordinates.txt should be a table with at least 3 columns: longitude, latitude, sitename (whatever you want, for file naming)

# read your site coordinates into an R data frame
wthfiles <- read.table(mysitecoordinates.txt)


#### ping the DayMet server to download your files
# make sure the R working directory has a folder called "weather" to hold the resulting files!
for (i in 1:nrow(wthfiles))
{
  download.file(
    url=paste0("https://daymet.ornl.gov/single-pixel/api/data?lat=", wthfiles[i,"latitude"],"&lon=", wthfiles[i,"longitude"], "&vars=tmax,tmin,prcp,srad&start=1980-01-01&end=2017-12-31"),
    destfile=paste0("weather/", wthfiles[i,"sitename"], "_", wthfiles[i,"longitude"], "_", wthfiles[i,"latitude"], ".dmw")
  )
}


#### now convert the DayMET .dmw files into DayCent .wth files
mydmw <- list.files(path = "weather", pattern = "dmw", full.names = T)  ## this gets all of the dmw filenames that were just created

library(lubridate)

for (j in 1:length(mydmw))
{
  dmw <- read.table(file=mydmw[j], skip = 7, header=T, sep=",")
  
  dmw$date <- as.Date(dmw$yday-1, origin=paste(dmw$year,"01","01", sep="-")) #converts year-doy to a date-format
  
  wth <- cbind(mday(dmw$date), month(dmw$date), year(dmw$date), yday(dmw$date), dmw$tmax..deg.c., dmw$tmin..deg.c., dmw$prcp..mm.day./10)
  
  write.table(
    x=wth,
    file=paste0("weather/", wthfiles[i,"sitename"], "_", wthfiles[i,"longitude"], "_", wthfiles[i,"latitude"], ".wth"), quote=F, row.names=F, col.names=F, sep="\t")
