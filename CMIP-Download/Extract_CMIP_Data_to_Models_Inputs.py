# This Python script converts downloaded CMIP data — including minimum and maximum air temperature,
# precipitation, solar radiation, wind speed, and relative humidity — into input files for the Ecosys, AgroIBIS, and Daycent models.
# Before running, ensure you have downloaded the CMIP data (see the readme for instructions)
# and stored it in the downloaded_CMIP_source_dir.
# The script processes data in parallel for efficiency, saves the converted outputs to designated directories,
# and handles leap years to ensure proper formatting for each model.

# The generated data will be organized in the below way:
# - converted_climate_data
#     - generated_AgroIBIS_climate_data
#         - experiment_ID
#             - site_ID
#                 - {var}_{year}.nc
#     - generated_Daycent_climate_data
#         - experiment_ID
#             - site_ID
#                 - DayCent_weather_{year}.txt
#     - generated_Ecosys_climate_data
#         - experiment_ID
#             - site_ID
#                 - me{year}w.csv
import os
import traceback
import csv
import numpy as np
import xarray as xr
import pandas as pd
import calendar
import datetime
from multiprocessing import Pool, cpu_count

# Define the necessary variables used in the code
wor_dir = '/work/hdd/bbkc/langzhou/CMIP_to_Model_Inputs/'                   # Directory where the project locates
downloaded_CMIP_source_dir = os.path.join(wor_dir, 'downloaded_CMIP_data')  # Directory where the downloaded CMIP data is stored

# Array of latitude and longitude for the given sites
lons = [-88.21]
lats = [40.07]
number_of_sites = len(lons)

source_ID = 'CESM2'                     # CMIP source ID  
variant_label = 'r10i1p1f1'             # CMIP variant label
grid_label = 'gn'                       # CMIP grid label
start_year = 2015                       # Start year for the CMIP data
end_year = 2100                         # End year for the CMIP data
year_interval = 10                      # Interval of years in the downloaded CMIP data
experiment_IDs = ['ssp245', 'ssp585']   # CMIP experiment IDs
frequency = 'day'                       # Frequency of the data


variables = ['tasmax', 'tasmin', 'hurs', 'sfcWind', 'pr', 'rsds']  # Variables to be extracted from CMIP data
var_map = {
    'tasmax': 'min_temperature',        # it is Kelvin in CMIP, and has been converted to Celsius
    'tasmin': 'max_temperature',        # it is Kelvin in CMIP, and has been converted to Celsius
    'hurs': 'relative_humidity',        # %
    'sfcWind': 'wind_speed',            # m/s
    'pr' : 'precipitation',             # it is mm/s in CMIP, and has been converted to mm/day
    'rsds': 'solar_radiation'           # W/m^2
}

units_map = {
    'tasmax': 'deg C',   
    'tasmin': 'deg C', 
    'hurs': 'percent',
    'sfcWind': 'm/s',
    'pr': 'mm',
    'rsds': 'W/m**2'  
}

var_to_AgroIBIS_map = {
    'tasmax' : 'tmax',
    'tasmin' : 'tmmn',
    'hurs': 'relh',
    'sfcWind': 'vs',
    'pr' : 'prec',
    'rsds' : 'rads'
}

# Define the dir where the converted data stored
generated_climate_dir = 'converted_climate_data'
generated_Ecosys_climate_dir = os.path.join(wor_dir, generated_climate_dir, 'generated_Ecosys_climate_data')
if not os.path.exists(generated_Ecosys_climate_dir):
    os.makedirs(generated_Ecosys_climate_dir, exist_ok=True)
generated_Daycent_climate_dir = os.path.join(wor_dir, generated_climate_dir, 'generated_Daycent_climate_data')
if not os.path.exists(generated_Daycent_climate_dir):
    os.makedirs(generated_Daycent_climate_dir, exist_ok=True)
Daycent_weather_prefix = 'DayCent_weather_'
generated_AgroIBIS_climate_dir = os.path.join(wor_dir, generated_climate_dir, 'generated_AgroIBIS_climate_data')
if not os.path.exists(generated_AgroIBIS_climate_dir):
    os.makedirs(generated_AgroIBIS_climate_dir, exist_ok=True)
    
# This is the function that each worker will run for a specific task.
# each worker will read the CMIP data for a specific site, experiment, variable, and time interval
# e.g., hurs_day_CESM2_ssp245_r10i1p1f1_gn_20150101-20241231.nc
# It returns the data for that site, experiment, variable, time interval (start year and end year), and the data itself.
# The data is a np array with length of time interval (number of years in that interval), 
# and each element is a xr.DataArray object for that variables in a year, e.g., tasmax for 2015, tasmax for 2016, ..., tasmax for 2024
def read_CMIP_data_worker(args):
    site_idx, exp_idx, var_idx, cur_interval_start, cur_interval_end, file_path = args
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Source file {file_path} does not exist.')
    var = variables[var_idx]
    cur_interval_data = np.empty((cur_interval_end-cur_interval_start+1), dtype=object)
    try:
        lon = lons[site_idx] if lons[site_idx] >= 0 else lons[site_idx] + 360 # adjust longitude for negative values
        lat = lats[site_idx]
        with xr.open_dataset(file_path, engine='netcdf4') as temp:
            cropped_data = temp.sel(lat=lat, lon=lon, method='nearest')
            if 'lev' not in cropped_data.dims:
                cropped_data = cropped_data.expand_dims('lev')
            cropped_data = cropped_data.assign_coords(lev = [1])
            cropped_data[var] = cropped_data[var].astype('double')
            if var in ['tasmax', 'tasmin']:
                cropped_data[var] = cropped_data[var] - 273.15 # convert Kelvin to Celsius
            elif var == 'pr':
                cropped_data[var] = cropped_data[var] * 86400  # convert from mm/s to mm/day
            elif var == 'hurs':
                cropped_data[var] = cropped_data[var].where(cropped_data[var] <= 100, 100) # set the up bound of hurs to 100%
            cropped_data[var].attrs["units"] = units_map[var]
            if 'nbnd' in cropped_data.dims:
                vars_with_nbnd = [v for v in cropped_data.data_vars if 'nbnd' in cropped_data[v].dims]
                cropped_data = cropped_data.drop_vars(vars_with_nbnd)
            cropped_data = cropped_data.transpose("time", "lev")
            # extract each year's var data
            grouped_data = cropped_data.groupby('time.year')
            for year in range(cur_interval_start, cur_interval_end + 1):
                if year not in grouped_data.groups:
                    raise ValueError(f"Year {year} not found in dataset.")
                yearly_data = cropped_data.isel(time=grouped_data.groups[year])
                # Convert cftime no-leap dates to pandas timestamps (standard calendar)
                old_times = yearly_data.time.values
                new_times = []
                for old_time in old_times:
                    # Extract year, month, day from cftime object
                    new_time = pd.Timestamp(year=old_time.year, month=old_time.month, day=old_time.day)
                    new_times.append(new_time)
                # Create new dataset with standard calendar timestamps
                yearly_data_standard = yearly_data.copy()
                yearly_data_standard = yearly_data_standard.assign_coords(time=new_times)
                # If it's a leap year, add Feb 29
                if calendar.isleap(year):
                    # Find Feb 28 and Mar 1 positions
                    val_feb_28 = yearly_data_standard[var].isel(time=58)
                    val_mar_01 = yearly_data_standard[var].isel(time=59)
                    avg_val = 0.5 * (val_feb_28 + val_mar_01)
                    # Create Feb 29 timestamp
                    feb_29_time = pd.Timestamp(year=year, month=2, day=29)
                    # Create a single-day dataset for Feb 29
                    feb_29_data = yearly_data_standard.isel(time=58)  # Use Feb 28 as template
                    feb_29_data = feb_29_data.expand_dims('time')
                    feb_29_data = feb_29_data.assign_coords(time=[feb_29_time])
                    feb_29_data[var] = feb_29_data[var] * 0 + avg_val  # Replace data with avg_val
                    # Combine original yearly data with Feb 29 data
                    yearly_data_with_leap = xr.concat([yearly_data_standard, feb_29_data], dim='time')
                    yearly_data_with_leap = yearly_data_with_leap.sortby('time')
                    cur_interval_data[year - cur_interval_start] = yearly_data_with_leap
                else:
                    cur_interval_data[year - cur_interval_start] = yearly_data_standard
        return (site_idx, exp_idx, var_idx, cur_interval_start, cur_interval_end, cur_interval_data)
    except Exception as e:
        print(f"Error processing {file_path} for site {site_idx}: {e}")
        print(traceback.format_exc())
        return (site_idx, exp_idx, var_idx, cur_interval_start, cur_interval_end, np.array([]))

# This sets up and runs the parallel job
# The function returns a 4D array of shape (number_of_experiments, number_of_sites, number_of_years, len(variables)
# Each element represents the climate data (a xr.DataArray object) for a particular experiment, site, year, and variable
def extract_CMIP_data_parallel():
    num_years = end_year - start_year + 1
    CMIP_data = np.empty((len(experiment_IDs), number_of_sites, num_years, len(variables)), dtype=object)
    # Step 1: Create task list
    tasks = []
    for exp_idx, exp_id in enumerate(experiment_IDs):
        for site_idx in range(number_of_sites):
            for year in range(start_year, end_year + 1, year_interval):
                year_idx = (year - start_year) // year_interval
                cur_interval_start = start_year + year_idx * year_interval
                cur_interval_end = cur_interval_start + year_interval - 1
                suffix = f'{cur_interval_start}0101-{cur_interval_end}1231' if cur_interval_end <= end_year else f'{cur_interval_start}0101-{end_year+1}0101'
                for var_idx, var in enumerate(variables):
                    file_name = f'{var}_{frequency}_{source_ID}_{exp_id}_{variant_label}_{grid_label}_{suffix}.nc'
                    file_path = os.path.join(downloaded_CMIP_source_dir, file_name)
                    tasks.append((site_idx, exp_idx, var_idx, cur_interval_start, min(cur_interval_end, end_year), file_path))
    # Step 2: Run in parallel to read CMIP data
    with Pool() as pool:
        results = pool.map(read_CMIP_data_worker, tasks)
    # Step 3: Fill CMIP_data array
    for site_idx, exp_idx, var_idx, cur_interval_start, cur_interval_end, data in results:
        if data is None or len(data) == 0:
            continue
        try:
            start_year_idx = cur_interval_start - start_year
            end_year_idx = cur_interval_end - start_year
            CMIP_data[exp_idx, site_idx, start_year_idx : end_year_idx+1, var_idx] = data
        except Exception as e:
            print(f"[ERROR] Failed to store data: {e}")
    return CMIP_data

# This function calculates the time of solar noon for a given longitude and latitude
# used for the Ecosys inputs
def calculate_time_of_solar_noon(lon, lat):
    gridsize = 0.125
    # define the lons and lats array to calculate the time of solar noon
    lons_array = np.arange(-124.938, -67.062, gridsize)
    lats_array = np.arange(  25.063,  52.939, gridsize)
    Lon_init = lons_array[0] - gridsize / 2
    idx = ((lon - Lon_init) / gridsize).astype('int')
    ZNOONG = (12 - lons_array[idx]/15.0 + 1)
    return ZNOONG

# This function take the CMIP_data as input, and convert it into Ecosys model inputs
def convert_CMIP_data_into_Ecosys_model_inputs(CMIP_data, generated_Ecosys_climate_dir):
    for exp_idx, exp_id in enumerate(experiment_IDs):
        for site_idx in range(number_of_sites):
            ZNOONG = calculate_time_of_solar_noon(lons[site_idx], lats[site_idx])
            exp_site_dir = os.path.join(generated_Ecosys_climate_dir, exp_id, f'site_{site_idx+1}')
            if not os.path.exists(exp_site_dir):
                os.makedirs(exp_site_dir)
            for year in range(start_year, end_year + 1):
                weather_csv = os.path.join(exp_site_dir, f'me{year}w.csv')
                headers = [
                    ['DJ0206XDMNHWPR'],
                    ['CCRSMW'],
                    [10, 0, ZNOONG],
                    [7, 0.25, 0.3, 0.05, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
                cur_year_climate_data = CMIP_data[exp_idx, site_idx, year-start_year]
                n_days = 366 if calendar.isleap(year) else 365
                year_col = [year] * n_days
                doy_col = [doy+1 for doy in range(0, n_days)]
                # Extract daily values for each climate variable
                climate_data_cols = []
                for var_idx, var in enumerate(variables):
                    cur_climate_var_data = cur_year_climate_data[var_idx][var].values
                    climate_data_cols.append(cur_climate_var_data)
                # Transpose to rows: each row is [year, doy, 'tasmax', 'tasmin', 'hurs', 'sfcWind', 'pr', 'rsds']
                rows = []
                for i in range(n_days):
                    row = [year_col[i], 
                           doy_col[i], 
                           climate_data_cols[0][i].item(), 
                           climate_data_cols[1][i].item(), 
                           climate_data_cols[2][i].item(), 
                           climate_data_cols[3][i].item(), 
                           climate_data_cols[4][i].item(),
                           climate_data_cols[5][i].item()]
                    rows.append(row)
                with open(weather_csv, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(headers)
                    writer.writerows(rows)

# This function take the CMIP_data as input, and convert it into AgroIBIS model inputs
def convert_CMIP_data_into_AgroIBIS_model_inputs(CMIP_data, generated_AgroIBIS_climate_dir):
    for exp_idx, exp_id in enumerate(experiment_IDs):
        for site_idx in range(number_of_sites):
            exp_site_dir = os.path.join(generated_AgroIBIS_climate_dir, exp_id, f'site_{site_idx+1}')
            if not os.path.exists(exp_site_dir):
                os.makedirs(exp_site_dir)
            for year in range(start_year, end_year + 1):
                cur_year_climate_data = CMIP_data[exp_idx, site_idx, year-start_year]
                for var_idx, var in enumerate(variables):
                    var_AgroIBIS = var_to_AgroIBIS_map[var]
                    outfile = os.path.join(exp_site_dir, f'{var_AgroIBIS}_{year}.nc')
                    cur_climate_var_data = cur_year_climate_data[var_idx]
                    cur_climate_var_data = cur_climate_var_data.rename({var : var_AgroIBIS})
                    cur_climate_var_data[[var_AgroIBIS, 'time', 'lev', 'lat', 'lon']].to_netcdf(outfile, format = "NETCDF4_CLASSIC")

# This function take the CMIP_data as input, and convert it into Daycent model inputs
def convert_CMIP_data_into_Daycent_model_inputs(CMIP_data, generated_Daycent_climate_dir):
    if not os.path.exists(generated_Daycent_climate_dir):
        os.makedirs(generated_Daycent_climate_dir)
    for exp_idx, exp_id in enumerate(experiment_IDs):
        for site_idx in range(number_of_sites):
            exp_site_dir = os.path.join(generated_Daycent_climate_dir, exp_id, f'site_{site_idx+1}')
            if not os.path.exists(exp_site_dir):
                os.makedirs(exp_site_dir)
            for year in range(start_year, end_year + 1):
                weather_file = os.path.join(exp_site_dir, f'{Daycent_weather_prefix}{year}.txt')
                cur_year_climate_data = CMIP_data[exp_idx, site_idx, year-start_year]
                n_days = 366 if calendar.isleap(year) else 365
                rows = []
                for i in range(n_days):
                    date = datetime.datetime(year, 1, 1) + datetime.timedelta(days=i)
                    month = date.month
                    day = date.day
                    doy = i + 1
                    row = [day, month, year, doy,   # 'tasmax', 'tasmin', 'pr', 'rsds', 'hurs', 'sfcWind'
                           round(cur_year_climate_data[0]['tasmax'].values[i].item(), 2),
                           round(cur_year_climate_data[1]['tasmin'].values[i].item(), 2),
                           round(cur_year_climate_data[4]['pr'].values[i].item(), 2),
                           round(cur_year_climate_data[5]['rsds'].values[i].item(), 4),
                           round(cur_year_climate_data[2]['hurs'].values[i].item(), 2),
                           round(cur_year_climate_data[3]['sfcWind'].values[i].item(), 4)]
                    rows.append(row)
                df = pd.DataFrame(rows)
                df.to_csv(weather_file, sep='\t', index=False, header=False)

if __name__ == '__main__':
    CMIP_data = extract_CMIP_data_parallel()
    ## save the data to a file
    # np.save(os.path.join(wor_dir, 'Extracted_CMIP_data.npy'), CMIP_data)
    ## load the data from a file
    # CMIP_data = np.load(os.path.join(wor_dir, 'Extracted_CMIP_data.npy'), allow_pickle=True)
    convert_CMIP_data_into_Ecosys_model_inputs(CMIP_data, generated_Ecosys_climate_dir)
    convert_CMIP_data_into_AgroIBIS_model_inputs(CMIP_data, generated_AgroIBIS_climate_dir)
    convert_CMIP_data_into_Daycent_model_inputs(CMIP_data, generated_Daycent_climate_dir)