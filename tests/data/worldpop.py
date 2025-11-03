import logging
from pathlib import Path

from dhis2eo.data import worldpop
from dhis2eo.org_units import from_file

DATA_DIR = Path(__file__).parent.parent / 'test_data'

# set verbose logging (hacky for now)
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more details
)

def test_download_population_data():
    geojson_file = DATA_DIR / 'geoBoundaries-MWI-ADM2.geojson'
    org_units = from_file(geojson_file, org_unit_id_col=None, name_col='shapeName', level=2)
    iso = 'MWI'
    year = 2030
    data = worldpop.get_population_data(year, iso)
    logging.info(f'pop data {data.to_xarray()}')
