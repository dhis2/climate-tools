%reset -f
import rasterio
import numpy as np
import xarray as xr
import pandas as pd
import geopandas as gpd
import re

# Define file paths
population_tiff_path = '/div/qbo/users/soucho/hisp_srilanka/GHS_POP_E2020_SriLanka_reprojected.tif'
shape_raster_tiff_path = '/div/qbo/users/soucho/hisp_srilanka/shape_raster.tif'
# Open the shape raster for reading and writing
with rasterio.open(shape_raster_tiff_path, 'r+') as shape_src:
    shape_data = shape_src.read(1)
    # Set all values > 0 to 1
    shape_data[shape_data > 0] = 1
    # Write the modified data back to the raster
    shape_src.write(shape_data, 1)
nc_file_path = '/div/qbo/users/soucho/hisp_srilanka/pmmake/qdm_corrected/pm25_qdm_rfr_sparseaware_monthly_static_2000-2023.nc'
output_excel_path = '/div/qbo/users/soucho/hisp_srilanka/pmmake/qdm_corrected/popwt_pm_ADM0.xlsx'

shapefile_path = '/div/qbo/users/soucho/hisp_srilanka/shapefiles/ADM0/geoBoundaries-LKA-ADM0.shp'

# Read the shapefile
shapefile_data = gpd.read_file(shapefile_path)
# shapefile_data['shapeISO_numeric'] = shapefile_data['shapeISO'].apply(lambda x: ''.join(re.findall(r'\d+', str(x))))
# shapefile_data['shapeISO_numeric'] = pd.to_numeric(shapefile_data['shapeISO_numeric'], errors='coerce')

print(shapefile_data.head())

# Open the NetCDF file and extract the time values
with xr.open_dataset(nc_file_path) as nc_data:
    lat = nc_data['lat'].values
    lon = nc_data['lon'].values
    time_values = pd.to_datetime(nc_data['time'].values)  # Convert time to pandas datetime
    variable_name = list(nc_data.data_vars.keys())[0]

# Open the population raster
with rasterio.open(population_tiff_path) as pop_src:
    population_data = pop_src.read(1)  # Read the first band
    pop_transform = pop_src.transform

# Open the shape raster
with rasterio.open(shape_raster_tiff_path) as shape_src:
    shape_data = shape_src.read(1)  # Read the first band
    shape_transform = shape_src.transform

# Ensure the dimensions of nc_data match the population and shape rasters
if population_data.shape != shape_data.shape:
    raise ValueError("The dimensions of the population raster and the shape raster do not match!")

# Get unique values in the shape raster (excluding 0 or negative values)
unique_values = np.unique(shape_data)
unique_values = unique_values[unique_values > 0]  # Exclude 0 and negative values

# Initialize a list to store results
all_results = []

# Iterate over each time slice in the NetCDF file
with xr.open_dataset(nc_file_path) as nc_data:
    for time_index, time_value in enumerate(time_values):
        print(f"Processing time slice {time_index + 1}/{len(time_values)}: {time_value}")
        nc_time_slice = np.flipud(nc_data[variable_name].isel(time=time_index).values)

        # Iterate over each unique value in the shape raster
        for value in unique_values:
            # Create a mask for the current unique value
            mask = shape_data == value

            # Extract the population and nc_data values corresponding to the mask
            masked_population = population_data[mask]
            masked_nc_data = nc_time_slice[mask]

            # Compute the weighted sum and the sum of the population, ignoring NaN values
            weighted_sum = np.nansum(masked_population * masked_nc_data)
            population_sum = np.nansum(masked_population)

            # Avoid division by zero
            if population_sum > 0:
                result = weighted_sum / population_sum
            else:
                result = np.nan  # Assign NaN if population_sum is zero

            # Append the result along with the corresponding date
            all_results.append({'Shape Value': value, 'Result': result, 'Date': time_value})

# Convert results to a DataFrame
results_df = pd.DataFrame(all_results)

# # Perform a left join to attach shapeName to results
# results_df = results_df.merge(
#     shapefile_data[['shapeISO_numeric', 'shapeName']],
#     left_on='Shape Value',
#     right_on='shapeISO_numeric',
#     how='left'
# )

# # Drop the redundant 'shapeISO_numeric' column
# results_df = results_df.drop(columns=['shapeISO_numeric'])

# # Write the updated DataFrame to an Excel file
# results_df.to_excel(output_excel_path, index=False)
# # Remove the word "District" from the shapeName column
# results_df['shapeName'] = results_df['shapeName'].str.replace('District', '', regex=False).str.strip()

# Write the updated DataFrame to an Excel file
results_df.to_excel(output_excel_path, index=False)

print(f"Results with updated shapeName written to {output_excel_path}")
print(f"Results with shapeName written to {output_excel_path}")