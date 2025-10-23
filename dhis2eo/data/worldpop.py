import requests
import tempfile
import logging
import sys
import os

import earthkit.data

logger = logging.getLogger(__name__)

# Since this module is so download centric, force all info logs to be printed
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_population_data(year, iso3):
    '''Downloads or gets from cache 100m data from worldpop v2 with estimates from 2015-2030'''
    
    # get iso3 from orgunits? 
    # ... 

    # generate url to download geotiff
    filename = f'{iso3.lower()}_pop_{year}_CN_100m_R2025A_v1.tif'
    url = f'https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/{year}/{iso3.upper()}/v1/100m/constrained/{filename}'
    
    # determine where the download will be cached
    cache_folder = tempfile.gettempdir()
    cache_path = os.path.join(cache_folder, filename)

    if os.path.exists(cache_path):
        logger.info(f'Loading from cache: {cache_path}')
        
        # load from the cached data
        data = earthkit.data.from_source('file', cache_path)

    else:
        # try to download the data and raise any errors
        logger.info(f'Downloading population data v2 from WorldPop...')
        resp = requests.get(url)
        resp.raise_for_status()

        # save to disk
        with open(cache_path, 'wb') as fobj:
            geotiff_bytes = resp.content
            fobj.write(geotiff_bytes)

        # load from the cached data
        data = earthkit.data.from_source('file', cache_path)

    # convert to xarray, clean data values
    xarr = data.to_xarray()
    xarr = xarr.rename_vars({'band_1': 'total_pop'})
    xarr = xarr.drop_vars('spatial_ref')

    # add year constant
    xarr = xarr.assign_coords(year=year)
    
    # return
    # TODO: return xarray instead of earthkit data, since hard to convert back unless saving back to disk
    return xarr
