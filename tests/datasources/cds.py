import logging

from dhis2eo.data import cds

# set verbose logging (hacky for now)
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more details
)

######################
# TODO: this is just some hacky tests, needs to be made into proper pytest

def test_download_daily_era5_data():
    bbox = [-13.3, 6.9, -10.3, 10.0]
    data = cds.download_daily_era5_data(2016, 1, bbox)

def test_get_daily_era5_data():
    # TODO: how to set and use a clean cache dir
    bbox = [-13.3, 6.9, -10.3, 10.0]
    # get first time
    data1 = cds.get_daily_era5_data(2016, 1, bbox) #, cache_folder='...')
    # get again
    data2 = cds.get_daily_era5_data(2016, 1, bbox) #, cache_folder='...')
    # test that both are read from the same cache file
    assert data1.path == data2.path
