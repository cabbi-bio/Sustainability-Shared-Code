### THIS SCRIPT will retrieve the SSURGO map unit for a set of long/lat coordinate pairs and create the filename for the existing DayCent soils.in file
### simsites needs to have latitude and longitude, the loop will then ping the USDA SSURGO server to find out which "map unit" represents that coordinate pair
# it will then construct the correct filename for the corresponding soils.in file as stored on the UI Biocluster
# IT DOES NOT create soils.in files themselves, those files already exist for the Continental US and are currently located on the Biocluster at:
# /home/groups/cabbi/Sustainability/EcoModelling/Lab_Groups/Hudiburg/jkent/ml/soils_SSURGO2019

library(soilDB) # You will need to use the Soil Database Interface to read data from the USDA-NRCS and NCSS databases
simsites <- data.frame(
  lat = NA,  ## replace NA with actual site latitudes
  long = NA,  ## replace NA with site longitudes
  mukey = NA, ## This will be filled in the script
  muname = NA ## This will be filled in the script
)

### this needs an internet connection to query the USDA server
ptm <- proc.time()

for (i in 1:nrow(simsites))
{
  if(i%%1000==0) { cat("Starting site",i,"\n")}
  ## LAT/LONG PAIR > MAPUNIT > COMPONENT (mukey=foreign key) > CHORIZON (cokey=foreign key)
  mylong <- simsites[i,"long"]
  mylat <- simsites[i,"lat"]
  #construct coordinate query to map unit table
  q <- paste0("SELECT mukey, muname FROM mapunit WHERE mukey IN ( SELECT * from SDA_Get_Mukey_from_intersection_with_WktWgs84('point(",mylong," ",mylat,")'))")  #construct SQL query to get map unit key for lonlat pair
  res <- suppressMessages( SDA_query(q) )  # get it from the SSURGO server
  if(is.null(res)) { next }
  simsites[i,"mukey"] <- res$mukey
  simsites[i,"muname"] <- res$muname
  soildir <- floor(simsites[i,"mukey"]/1000)  #naming convention for subdirectories -- floor is like round, but simply chops off digits rather than rounding them  
  simsites[i,"soilsin"] <- paste0(soildir,"/",simsites[i,"mukey"],".in")  #paste the folder together with the actual filename
  
}
proc.time() - ptm

write.table(simsites,file="simsites_SSURGO_soilsin.tsv",sep="\t",quote=F,row.names=F)
