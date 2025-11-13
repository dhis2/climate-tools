import requests
import tempfile
import logging
import sys
import os

import xarray as xr

from ..utils import netcdf_cache

logger = logging.getLogger(__name__)

# Since this module is so download centric, force all info logs to be printed
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@netcdf_cache()
def get(year, iso3):
    '''Downloads or gets 100m population count data from worldpop v2 with estimates from 2015-2030'''

    # generate url to download geotiff
    filename = f'{iso3.lower()}_pop_{year}_CN_100m_R2025A_v1.tif'
    url = f'https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/{year}/{iso3.upper()}/v1/100m/constrained/{filename}'
    
    # determine where to download to
    download_folder = tempfile.gettempdir()
    download_path = os.path.join(download_folder, filename)

    # try to download the data and raise any errors
    logger.info(f'Downloading population data v2 from WorldPop...')
    resp = requests.get(url)
    resp.raise_for_status()

    # save to disk
    with open(download_path, 'wb') as fobj:
        geotiff_bytes = resp.content
        fobj.write(geotiff_bytes)

    # load downloaded file as xarray
    xarr = xr.open_dataset(download_path)

    # clean data values
    xarr = xarr.rename_vars({'band_data': 'total_pop'})
    xarr = xarr.drop_vars(['spatial_ref', 'band'])

    # add year constant
    xarr = xarr.assign_coords(year=year)
    
    # return
    return xarr
