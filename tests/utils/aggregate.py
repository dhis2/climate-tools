import earthkit.data

import dhis2eo.org_units
import dhis2eo.utils.aggregate

from datetime import date
from pathlib import Path
import logging

DATA_DIR = Path(__file__).parent.parent / 'test_data'

def test_aggregate_to_time_period_daily_to_monthly():
    # load data
    daily_data_path = DATA_DIR / 'era5-land-daily-mean-temperature-2m-july-2025-sierra-leone.nc'
    data = earthkit.data.from_source('file', daily_data_path)
    logging.info(data.to_xarray())

    # aggregate
    period_type = 'monthly'
    variables = {'t2m': 'mean'}
    agg = dhis2eo.utils.aggregate.to_time_periods(data, variables, period_type)
    logging.info(agg)
