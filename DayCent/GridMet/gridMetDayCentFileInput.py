import os
import sys
import numpy as np
import pandas as pd
import subprocess

# This is a Python script that will take a comma-delimited file that contains a list of lat/lon coordinates to get gridMET data and put it in DayCent format. 
# The file should have the following columns: LocationName, Latitude, Longitude
# For questions, email Leslie Stoecker, lensor@illinois.edu

# Inputs to change
syr = '2019' # First year to pull data. The first year in the dataset is 1979.
eyr = '2020' # Last year to pull data. There is current data, but it is not finalized currently.
dir = 'C:\\Users\\IGB\\Box\\Sustainability Hub\\GridMet Data Download\\' # Directory where all the files will be stored
delim = '\\' # Customizable file/directory delimiter depending on the system you are running it on
filename = 'DayCent_Locations.csv' # Comma-delimited file with the following columns: LocationName, Latitude, Longitude

# Open the DayCent Location File and put it in an array
locationArray = np.loadtxt(filename, delimiter=',', dtype=str)

# Loop through each line of the file and pass the lat/lon to gridMetDayCent.py to get the data
for line in locationArray:
    if line[0] == 'LocationName': continue

    subprocess.run(['python', 'gridMetDayCent.py', syr, eyr, line[1], line[2], dir, line[0], delim])
    print('Finished: ' + line[0])
