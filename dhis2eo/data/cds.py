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

# TODO: Maybe switch to lookup for different datasets
DEFAULT_DAILY_ERA5_DATA_DICT = {
    'daily_mean': ['2m_temperature'], 
    'daily_sum': ['total_precipitation'], 
}

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

def get_daily_era5_data(year, month, org_units=None, bbox=None, data_dict=None, cache_folder=None):
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

def download_daily_era5_data(year, month, org_units=None, bbox=None, data_dict=None):
    '''Download daily era5 data'''
    # TODO: maybe support downloading a whole year, since it's allowed for this dataset... 
    # TODO: maybe support not specifying a subregion/area to get the whole world, but unnecessary...? 
    # get default data
    data_dict = data_dict or DEFAULT_DAILY_ERA5_DATA_DICT
    # get or calculate bbox
    if bbox is None:
        if org_units is not None:
            bbox = list(org_units.total_bounds)
        else:
            raise Exception('Either org_units or bbox have to be set')
    # extract the coordinates from input bounding box
    xmin,ymin,xmax,ymax = bbox
    # download one statistics type at a time
    data_list = []
    for stat_type,variables in data_dict.items():
        # construct the query parameters
        params = {
            "product_type": "reanalysis",
            "variable": variables,
            "year": str(year),
            "month": [str(month).zfill(2)],
            "daily_statistic": stat_type,
            "time_zone": "utc+00:00",
            "frequency": "1_hourly", # Warning: This may not be allowed for all variables... 
            "area": [ymax, xmin, ymin, xmax], # notice how we reordered the bbox coordinate sequence
            "data_format": "netcdf",
            "download_format": "unarchived",
        }
        _,last_day = calendar.monthrange(year, month)
        params['day'] = [str(day).zfill(2) for day in range(1, last_day)]
        # download the data
        logger.info(f'Downloading {stat_type} data from CDS API...')
        logger.info(f'Request parameters: \n{json.dumps(params)}')
        data = earthkit.data.from_source("cds",
            "derived-era5-single-levels-daily-statistics",
            **params
        )
        data_list.append(data)
    # merge the data into one
    merged = data_list[0]
    if len(data_list) > 1:
        for data in data_list[1:]:
            # earthkit supports concatenating datasets with + operator
            merged += data
    # return
    return merged
