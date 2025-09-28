from datetime import datetime
import pandas as pd

from ..utilities.time import detect_period_type, YEAR, MONTH, WEEK, DAY

def parse_period(period_value):
    '''Convert pandas period or datetime values to DHIS2 period type'''
    # TODO: more robust handling and testing of period formats and types
    period_string = str(period_value).split(' ')[0] # remove time info after space
    period_type = detect_period_type(period_string)
    if period_type == DAY:
        period_obj = pd.Period(period_value, freq='D')
        return period_obj.strftime('%Y%m%d')
    else:
        raise NotImplementedError(f'Period type {period_type} not yet supported')

def df_to_dhis2_json(df, data_element_id, org_unit_col, period_col, value_col):
    '''Translates a pandas.DataFrame to JSON format used by DHIS2 Web API.'''
    # subset the df
    df_subset = df[[org_unit_col, period_col, value_col]]

    # remap column names
    remap = {
       org_unit_col: 'orgUnit',
       period_col: 'period',
       value_col: 'value',
    }
    df_subset.rename(columns=remap, inplace=True)

    # parse period column to dhis2 format
    df_subset['period'] = df_subset['period'].apply(parse_period)

    # add dataElement column
    df_subset['dataElement'] = data_element_id

    # convert to list of dicts
    data = df_subset.to_dict(orient='records')
    return { "dataValues": data }
