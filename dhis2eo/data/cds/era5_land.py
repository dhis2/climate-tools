import earthkit.data
import geopandas as gpd
import hashlib
import json
import os
import tempfile
import logging
import calendar
from datetime import date
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

# Since this module is so download centric, force all info logs to be printed
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

DEFAULT_VARIABLES = [
    '2m_temperature',
    'total_precipitation',
]

# Try to fix cache issue by setting download threads to 1
config = earthkit.data.config
config.set('number-of-download-threads', 1)

def generate_cache_filename(dataset, year, data_dict, month=None, bbox=None):
    '''Generates a cache file name based on misc download parameters'''
    stubs = []
    # provider stub
    provider_stub = 'cds'
    stubs.append(provider_stub)
    # dataset stub
    stubs.append(dataset)
    # data dict stub
    data_dict_stub = 'params-' + hashlib.sha256(json.dumps(data_dict).encode('ascii')).hexdigest()[:6]
    stubs.append(data_dict_stub)
    # spatial stub if bbox is given
    if bbox:
        bbox_hash = hashlib.sha256(','.join(map(str, bbox)).encode('ascii')).hexdigest()[:6]
        stubs.append('region-' + bbox_hash)
    # time stub
    time_stub = f'{year}'
    if month:
        time_stub += f'-{str(month).zfill(2)}'
    stubs.append(time_stub)
    # join the stubs to final filename without extension
    filename = '_'.join(stubs)
    return filename

# TODO: old for era5 normal, redo for era5-land 
def _get_daily_era5_data(year, month, org_units=None, bbox=None, data_dict=None, cache_folder=None):
    '''Hardcoded cached version for daily era5 data'''
    # TODO: make into generic decorator that can be applied to any download function
    # ...needs to accept a dataset arg as well
    current_date = date.today()
    # get cache folder
    cache_folder = tempfile.gettempdir()
    # get or calculate bbox
    if bbox is None:
        if org_units is not None:
            bbox = org_units.total_bounds.tolist()
        else:
            raise Exception('Either org_units or bbox have to be set')
    # get default data dicts
    data_dict = data_dict or DEFAULT_DAILY_ERA5_DATA_DICT
    # convert input args to a cache filename
    file_name = generate_cache_filename('daily-era5', year, data_dict=data_dict, month=month, bbox=bbox)
    file_name += '.nc'
    file_path = os.path.join(cache_folder, file_name)
    # check if cache filename already exists
    if os.path.exists(file_path):
        # load from cache
        logger.info(f'Loading from cache: {file_path}')
        data = earthkit.data.from_source('file', file_path)
    else:
        # download data from the api
        data = download_daily_era5_data(year=year, month=month, data_dict=data_dict, org_units=org_units)
        # save to cache, but not if we're still in the current month
        if year == current_date.year and month == current_date.month:
            logger.info('Data is for the current month and will not be cached, since data is added daily')
        else:
            logger.info(f'Saving to cache: {file_path}')
            data.to_target('file', file_path)
            # Reload the data from the cache to ensure same .path attr
            # Warning: a little hacky... 
            data = earthkit.data.from_source('file', file_path)
    # return
    return data

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
    # return
    return data

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
    # return
    return data

def get(period_type, **kwargs):
    '''Download era5-land data a period type'''
    if period_type == 'hourly':
        return get_hourly(**kwargs)
    elif period_type == 'monthly':
        return get_monthly(**kwargs)
    else:
        raise ValueError(f'Unsupported period type {period_type}')
