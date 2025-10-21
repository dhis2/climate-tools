import os
import logging
from pathlib import Path

from dhis2eo.data import cds
from dhis2eo.org_units import from_file

DATA_DIR = Path(__file__).parent.parent / 'test_data'

# set verbose logging (hacky for now)
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more details
)

######################
# TODO: this is just some hacky tests, needs to be made into proper pytest
# TODO: how to set and use a clean cache dir

def test_download_daily_era5_data():
    geojson_file = DATA_DIR / 'geoBoundaries-MWI-ADM2.geojson'
    org_units = from_file(geojson_file, org_unit_id_col=None, name_col='shapeName', level=2)
    data = cds.download_daily_era5_data(2016, 1, org_units)

def test_get_daily_era5_data():
    geojson_file = DATA_DIR / 'geoBoundaries-MWI-ADM2.geojson'
    org_units = from_file(geojson_file, org_unit_id_col=None, name_col='shapeName', level=2)
    # get first time
    data1 = cds.get_daily_era5_data(2016, 1, org_units) #, cache_folder='...')
    # get again
    data2 = cds.get_daily_era5_data(2016, 1, org_units) #, cache_folder='...')
    # test that both are read from the same cache file
    assert data1.path == data2.path
