import json
import logging
import earthkit.data
import xarray as xr

from ...utils import netcdf_cache, force_logging

logger = logging.getLogger(__name__)
force_logging(logger)

DEFAULT_VARIABLES = [
    '2m_temperature',
    'total_precipitation',
]

# Try to fix CDS cache issue by setting download threads to 1
config = earthkit.data.config
config.set('number-of-download-threads', 1)

@netcdf_cache
def get(years, months, org_units=None, bbox=None, variables=None):
    '''Download monthly era5-land data'''

    # get default variables
    variables = variables or DEFAULT_VARIABLES

    # get or calculate bbox
    if bbox is None:
        if org_units is not None:
            bbox = list(org_units.total_bounds)
        else:
            raise Exception('Either org_units or bbox have to be set')
    
    # extract the coordinates from input bounding box
    xmin,ymin,xmax,ymax = bbox

    # construct the query parameters
    params = {
        "product_type": ["monthly_averaged_reanalysis"],
        "variable": variables,
        "year": [str(year) for year in years],
        "month": [str(month).zfill(2) for month in months],
        "time": ["00:00"],
        "area": [ymax, xmin, ymin, xmax], # notice how we reordered the bbox coordinate sequence
        "data_format": "netcdf",
        "download_format": "unarchived",
    }

    # download the data
    logger.info(f'Downloading data from CDS API...')
    logger.info(f'Request parameters: \n{json.dumps(params)}')
    data = earthkit.data.from_source("cds",
        "reanalysis-era5-land-monthly-means",
        **params
    )

    # load lazily from disk using xarray
    data_array = xr.open_dataset(data.path)
    
    # return
    return data_array
