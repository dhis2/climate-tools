
from datetime import date

def get_last_imported_period_for_data_element_ids(client, data_element_ids, org_unit_level):
    '''Returns dict of each provided data element id with latest period containing data for a given org_unit_level.'''
    last_imported_dict = {}

    for data_element_id in data_element_ids:
        latest_period_response = client.analytics_latest_period_for_level(de_uid=data_element_id, level=org_unit_level)
        if latest_period_response['existing']:
            latest_period = latest_period_response['existing']['id']
            latest_year,latest_month = int(latest_period[:4]), int(latest_period[4:6])
            last_imported_dict[data_element_id] = (latest_year, latest_month)
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
        last_imported_year, last_imported_month = last_imported
        # synching is needed only if year and month is greater than last imported year and month
        needs_synching = (year > last_imported_year) and (month > last_imported_month)
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

# def import_data_to_dhis2(client, org_units, get_data_func, data_element_id, earliest_year, earliest_month):
#     import pandas as pd
#     import geopandas as gpd
#     from dhis2eo.integrations.pandas import dataframe_to_dhis2_json

#     bbox = org_units.total_bounds

#     # fetch, aggregate, and import data month-by-month
#     for year, month in iter_month_periods_since_last_data_value(data_element_id, earliest_year, earliest_month):
#         print('====================')
#         print('Period:', year, month)
#         # download data
#         print('Getting data...')
#         data = get_data_func(year, month, bbox)
#         # aggregate to org units
#         print('Aggregating...')
#         agg = aggregate(data, org_units, id_col='org_unit_id')

#         # TODO: allow custom postprocessing after download before import...
#         # convert to celsius
#         #agg['t2m'] -= 273.15
#         # ignore nan values
#         #agg = agg[~pd.isna(agg['t2m'])]

#         # convert to dhis2 json
#         payload = dataframe_to_dhis2_json(
#             df=agg,
#             org_unit_col='org_unit_id',
#             period_col='valid_time',
#             value_col='t2m',
#             data_element_id=data_element_id,
#         )
#         # upload to dhis2
#         print('Importing to DHIS2...')
#         res = client.post("/api/dataValueSets", json=payload)
#         print("Results:", res['response']['importCount'])

#     print('=====================')
#     print('Data import finished!')

# if __name__ == '__main__':
#     data_element_id = 'GbUpvHzCzn8' # data element id that you want to import data into
#     start_year = 2025
#     start_month = 1
#     import_data_to_dhis2(data_element_id, start_year, start_month)
