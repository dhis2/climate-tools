import json
from datetime import datetime

def get_org_unit_from_array_item(item, org_unit_dim = 'orgUnit'):
  return item.coords.get(org_unit_dim).data.item(0);  

# TODO: handle different period formats and types
def get_period_from_array_item(item, period_dim = 'period'):
  # 1e+9 converts from nanoseconds to seconds 
  return datetime.fromtimestamp(item.coords.get(period_dim).item(0) / 1e+9).strftime('%Y-%m-%d')

def get_value_from_array_item(item):
  return item.data.item(0);

# Translates an xarray.DataArray to JSON format used by DHIS2 Web API
def data_array_to_dhis2_json(data_array, data_element_id, org_unit_dim, period_dim):
  data = []
  for item in data_array:     
    data.append({
      'dataElement': data_element_id,
      'orgUnit': get_org_unit_from_array_item(item, org_unit_dim),
      'period': get_period_from_array_item(item, period_dim),  
      'value': get_value_from_array_item(item),
    })

  return json.dumps({ "dataValues": data })