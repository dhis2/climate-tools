import dhis2eo.org_units
import dhis2eo.synch
import dhis2eo.data.cds

from dhis2_client import DHIS2Client
from dhis2_client.settings import ClientSettings

from datetime import date
from pathlib import Path
import logging

DATA_DIR = Path(__file__).parent / 'test_data'

def init_client():
    # Create DHIS2 client connection
    cfg = ClientSettings(
        base_url="http://localhost:8080",
        username="admin",
        password="district"
    )
    client = DHIS2Client(settings=cfg)
    return client

def test_iter_dhis2_monthly_synch_status():
    # init dhsi2 client
    client = init_client()
    # define which data element ids to check
    # TODO: these should probably be created per test and maybe initialized with some test values...
    data_element_ids = ['gPPVvS6u23w', 'i9W7DhW60kK']
    # loop test months
    start_year = 2020
    start_month = 3
    org_unit_level = 2
    synch_status_list = []
    for month_synch_status in dhis2eo.synch.iter_dhis2_monthly_synch_status(client, start_year, start_month, data_element_ids, org_unit_level=org_unit_level):
        logging.info(month_synch_status)
        synch_status_list.append(month_synch_status)
    # test that first synch status is same as start year and month
    first_synch_status = synch_status_list[0]
    assert first_synch_status['year'] == start_year
    assert first_synch_status['month'] == start_month
    # test that last synch status is same as today
    current_date = date.today()
    last_synch_status = synch_status_list[-1]
    assert last_synch_status['year'] == current_date.year
    assert last_synch_status['month'] == current_date.month

def test_synch_dhis2_data():
    # init dhsi2 client
    client = init_client()
    
    # define the data element id and aggregatioin method for each variable to import
    # TODO: these should probably be created per test and maybe initialized with some test values...
    variables = {
        't2m': {'data_element_id': 'gPPVvS6u23w', 'method': 'mean'},
        'tp': {'data_element_id': 'i9W7DhW60kK', 'method': 'sum'},
    }
    
    # run the synch function
    start_year = 2025
    start_month = 5
    org_unit_level = 2
    dhis2eo.synch.synch_dhis2_data(
        client, 
        dhis2eo.data.cds.get_daily_era5_data, 
        start_year, 
        start_month, 
        variables=variables,
        org_unit_level=org_unit_level, 
    )
    
    # TODO: should probably check imported values
    # ... 
