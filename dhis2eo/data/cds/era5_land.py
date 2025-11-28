import json
import logging
import calendar
import earthkit.data
import xarray as xr

from ..utils import netcdf_cache, force_logging

logger = logging.getLogger(__name__)
force_logging(logger)

DEFAULT_VARIABLES = [
    '2m_temperature',
    'total_precipitation',
]

# Try to fix CDS cache issue by setting download threads to 1
config = earthkit.data.config
config.set('number-of-download-threads', 1)

def get_hourly(year, month, org_units=None, bbox=None, variables=None, days=None):
    '''Download hourly era5-land data'''

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
    _,last_day = calendar.monthrange(year, month)
    days = days or [day for day in range(1, last_day+1)]
    days = [str(day).zfill(2) for day in days]
    params = {
        "variable": variables,
        "year": str(year),
        "month": [str(month).zfill(2)],
        "day": days,
        "time": [f'{str(h).zfill(2)}:00' for h in range(0, 23+1)],
        "area": [ymax, xmin, ymin, xmax], # notice how we reordered the bbox coordinate sequence
        "data_format": "netcdf",
        "download_format": "unarchived",
    }

    # download the data
    logger.info(f'Downloading data from CDS API...')
    logger.info(f'Request parameters: \n{json.dumps(params)}')
    data = earthkit.data.from_source("cds",
        "reanalysis-era5-land",
        **params
    )

    # load lazily from disk using xarray
    data_array = xr.open_dataset(data.path)

    # return
    return data_array

def get_monthly(years, months, org_units=None, bbox=None, variables=None):
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

@netcdf_cache()
def get(period_type, **kwargs):
    '''Download era5-land data a period type'''
    if period_type == 'hourly':
        return get_hourly(**kwargs)
    elif period_type == 'monthly':
        return get_monthly(**kwargs)
    else:
        raise ValueError(f'Unsupported period type {period_type}')
