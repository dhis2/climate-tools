'''
Functionality to create a consistently structured geopandas.GeoDataFrame to represent organisation units.
Keeps only the following structured columns:
- org_unit_id
- name
- geom
'''

import geopandas as gpd
import json
import string
import random

# TODO: check and handle org units with different coordinate projections

def from_file(path, **kwargs):
    if str(path).endswith(('.geojson', '.json')):
        # load from geojson file
        with open(path) as fobj:
            geojson = json.load(fobj)
            org_units = from_geojson(geojson, **kwargs)
    
    elif str(path).endswith('.shp'):
        # load from shapefile
        org_units = from_shapefile(path, **kwargs)

    else:
        raise NotImplementedError(f'Unsupported file format: {path}')
    
    return org_units

def generate_org_unit_id():
    letters = string.ascii_letters  # A-Z, a-z
    chars = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return random.choice(letters).upper() + ''.join(random.choices(chars, k=10))

def standardize_org_units_geodataframe(org_units, org_unit_id_col, name_col, level):
    # auto generate org unit id if not given
    if org_unit_id_col is None:
        org_unit_id_col = 'org_unit_id'
        org_units[org_unit_id_col] = [generate_org_unit_id() for _ in range(len(org_units))]

    # add constant column with the org unit level
    org_units['level'] = level

    # rename and keep only common column names
    remap = {
        org_unit_id_col: 'org_unit_id',
        name_col: 'name',
    }
    org_units = org_units.rename(columns=remap)
    keep_cols = list(remap.values()) + ['level', 'geometry']
    org_units = org_units[keep_cols]

    # return
    return org_units

def from_geojson(org_units_geojson, org_unit_id_col, name_col, level):
    '''Create organisation unit GeoDataFrame from standard geojson.
    User must provide column names containing org unit id and name. 
    '''
    # input can either be geojson string or dicts
    
    # if geojson string, load as python dicts
    if isinstance(org_units_geojson, str):
        org_units_geojson = json.loads(org_units_geojson)

    # convert to geopandas
    org_units = gpd.GeoDataFrame.from_features(org_units_geojson["features"])

    # standardize GeoDataFrame
    org_units = standardize_org_units_geodataframe(org_units, org_unit_id_col, name_col, level)

    # return
    return org_units

def from_dhis2_geojson(org_units_geojson):
    '''Create organisation unit GeoDataFrame from DHIS2 geojson, 
    where the column names are already known. 
    '''
    # input can either be geojson string or dicts

    # if geojson string, load as python dicts
    if isinstance(org_units_geojson, str):
        org_units_geojson = json.loads(org_units_geojson)

    # copy dhis2 feature ids to org unit id column
    for feat in org_units_geojson['features']:
        if feat['id']:
            feat['properties']['org_unit_id'] = feat['id']

    # get org unit level from known dhis2 geojson property
    level = int(org_units_geojson['features'][0]['properties']['level'])

    # convert the geojson to geopandas using the standard dhis2 geojson column names
    org_units = from_geojson(
        org_units_geojson,
        org_unit_id_col='org_unit_id',
        name_col='name',
        level=level,
    )

    # return
    return org_units

def from_shapefile(shapefile_path, org_unit_id_col, name_col, level):
    '''Create organisation unit GeoDataFrame from shapefile.
    User must provide column names containing org unit id and name.
    '''
    # load with geopandas
    org_units = gpd.read_file(shapefile_path)

    # standardize GeoDataFrame
    org_units = standardize_org_units_geodataframe(org_units, org_unit_id_col, name_col, level)

    return org_units
