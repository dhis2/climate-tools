from dhis2eo.synch import iter_dhis2_monthly_synch_status

from dhis2_client import DHIS2Client
from dhis2_client.settings import ClientSettings

import logging

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
    for month_synch_status in iter_dhis2_monthly_synch_status(client, start_year, start_month, data_element_ids, org_unit_level=org_unit_level):
        logging.info(month_synch_status)
