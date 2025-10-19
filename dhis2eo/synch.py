
from datetime import date
import logging

from dhis2eo.integrations.pandas import dataframe_to_dhis2_json
from dhis2eo.utils.earthkit import aggregate_to_org_units

logger = logging.getLogger(__name__)

def get_last_imported_period_for_data_element_ids(client, data_element_ids, org_unit_level):
    '''Returns dict of each provided data element id with latest period containing data for a given org_unit_level.'''
    # TODO: maybe need to handle different period types? 
    last_imported_dict = {}

    for data_element_id in data_element_ids:
        latest_period_response = client.analytics_latest_period_for_level(de_uid=data_element_id, level=org_unit_level)
        if latest_period_response['existing']:
            latest_period = latest_period_response['existing']['id']
            latest_year,latest_month = int(latest_period[:4]), int(latest_period[4:6])
            last_imported_dict[data_element_id] = {'year': latest_year, 'month': latest_month}
        else:
            last_imported_dict[data_element_id] = None

    return last_imported_dict

def iter_months(start_year, start_month, end_year, end_month):
    '''Iterate months between start and end year and month.'''
    # loop years and months between start and end month
    for year in range(start_year, end_year + 1):
        for month in range(1, 12 + 1):
            # check outside of time scope
            if year == start_year and month < start_month:
                continue
            if year == end_year and month > end_month:
                continue
            # yield year-month pairs
            yield year,month

def iter_dhis2_monthly_synch_status(client, start_year, start_month, data_element_ids, org_unit_level):
    '''Iterate all months since start_month until today
    and return dict indicating the sync status for each data element id.'''
    # determine the last imported period for each provided data element id
    last_imported_dict = get_last_imported_period_for_data_element_ids(client, data_element_ids, org_unit_level)
    # get current year and month
    current_date = date.today()
    current_year,current_month = current_date.year, current_date.month
    # define how to check synch status
    def get_data_element_synch_status(year, month, data_element_id):
        last_imported = last_imported_dict[data_element_id]
        if last_imported is None:
            # no previous import detected, all months need synching
            return True
        # synching is needed only if month is greater than last imported month in current year, or year is greater than last imported year
        needs_synching = (year == last_imported['year'] and month > last_imported['month']) or (year > last_imported['year'])
        return needs_synching
    # loop months between start month and current month
    for year,month in iter_months(start_year, start_month, current_year, current_month):
        # check synch status of each data element id for this month
        synch_status = {
            data_element_id: get_data_element_synch_status(year, month, data_element_id)
            for data_element_id in data_element_ids
        }
        # yield dict of year, month, and synch_status
        yield {'year': year, 'month': month, 'synch_needed': synch_status}

def synch_dhis2_data(client, start_year, start_month, org_units, get_monthly_data_func, data_elements_to_variables):
    # fetch, aggregate, and import data month-by-month
    org_unit_level = org_units['level'].values[0] # TODO: is this the best approach? 
    data_element_ids = list(data_elements_to_variables.keys())
    for month_synch_status in iter_dhis2_monthly_synch_status(client, start_year, start_month, data_element_ids, org_unit_level):
        year,month,synch_needed_lookup = month_synch_status['year'], month_synch_status['month'], month_synch_status['synch_needed']
        logger.info('====================')
        logger.info(f'Period: {year}-{month}')
        # download data
        data_elements_needing_synch = [de for de,synch_needed in synch_needed_lookup.items() if synch_needed]
        if not data_elements_needing_synch:
            logger.info('All data elements up to date, no synch needed')
            continue
        logger.info('Getting data...')
        data = get_monthly_data_func(year, month, org_units)
        # aggregate to org units
        # aggregates up to multiple variables depending on what was downloaded
        logger.info('Aggregating...')
        agg = aggregate_to_org_units(data, org_units)
        # collect aggregated variables that need synching and convert to dhis2 json
        all_data_values = []
        for data_element_id in data_elements_needing_synch:
            variable = data_elements_to_variables[data_element_id]
            variable_data_values = dataframe_to_dhis2_json(
                df=agg,
                org_unit_col='org_unit_id', # better way to set this?
                period_col='valid_time', # TODO: this should be more robust to other column names...
                value_col=variable,
                data_element_id=data_element_id,
            )
            all_data_values.extend(variable_data_values['dataValues'])
        payload = {'dataValues': all_data_values}
        # upload to dhis2
        logger.info(f'Importing to DHIS2 data elements: {data_elements_needing_synch}...')
        #logger.info(f'Payload: {payload}')
        res = client.post("/api/dataValueSets", json=payload)
        logger.info("Results:", res['response']['importCount'])

    logger.info('=====================')
    logger.info('DHIS2 data synch finished!')
