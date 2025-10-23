
from pathlib import Path

from dhis2_client import DHIS2Client
from dhis2_client.settings import ClientSettings

from dhis2eo.org_units import from_file, from_dhis2_geojson

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

def assert_org_units_format(dataframe, level):
    # check that expected org unit column can be accessed
    dataframe['org_unit_id']
    dataframe['name']
    dataframe['level']
    # assert correct org unit level
    assert dataframe['level'].values[0] == level
    # assert each entry has a unique org unit id
    assert not dataframe['org_unit_id'].duplicated().any()

def test_from_file_geojson():
    file_path = DATA_DIR / 'geoBoundaries-MWI-ADM2.geojson'
    level = 2
    org_units = from_file(file_path, org_unit_id_col=None, name_col='shapeName', level=level)

    # assert
    assert_org_units_format(org_units, level=level)

def test_from_dhis2_geojson():
    # init dhsi2 client
    client = init_client()
    
    # get org units dhis2
    level = 2
    org_units_geojson = client.get_org_units_geojson(level=level)
    org_units = from_dhis2_geojson(org_units_geojson)

    # assert
    assert_org_units_format(org_units, level=level)

def test_from_file_shapefile():
    file_path = DATA_DIR / 'geoBoundaries-MWI-ADM2.shp'
    level = 2
    org_units = from_file(file_path, org_unit_id_col=None, name_col='shapeName', level=level)

    # assert
    assert_org_units_format(org_units, level=level)
