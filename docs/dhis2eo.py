import json
from datetime import datetime

def getOrgUnitFromItem(item):
  return item.coords.get('orgUnit').data.item(0);  

def getPeriodFromItem(item):
  # 1e+9 converts from nanoseconds to seconds 
  return datetime.fromtimestamp(item.coords.get('period').item(0) / 1e+9).strftime('%Y-%m-%d')

def getValueFormItem(item):
  return item.data.item(0);

# Translates an xarray.DataArray to the JSON format of the DHIS2 Web API
def dataArrayToJson(dataArray):
  data = []
  for item in dataArray:     
    data.append({
      'orgUnit': getOrgUnitFromItem(item),
      'period': getPeriodFromItem(item),  
      'value': getValueFormItem(item),
    })
  return json.dumps(data)