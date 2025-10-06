import pandas as pd
from datetime import date
import string
import random
import os

def geodataframe_to_dhis2_org_units(
    geodataframe, 
    country, 
    name_field,
    ):
    '''
    Limited to only the first subnational org unit level for now.
    Outputs both the json metadata and the geojson with geometries.
    '''
    dhis2_org_units = []

    # Convert to GeoJSON
    geojson = geodataframe.__geo_interface__

    # Generate UIDs
    def generate_uid():
        letters = string.ascii_letters  # A-Z, a-z
        chars = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
        return random.choice(letters).upper() + ''.join(random.choices(chars, k=10))

    # Create top-level country org unit
    country_uid = generate_uid()
    country_org_unit = {
        "id": country_uid,
        "name": country,
        "shortName": country,
        #"code": country_code,
        "openingDate": str(date.today()), # TODO: not sure if required, or if we can try to read this from the input? 
        "level": 1,
        #"featureType": "NONE"
    }
    dhis2_org_units.append(country_org_unit)

    # Now process each region feature
    for feature in geojson["features"]:
        props = feature["properties"]
        geom = feature["geometry"]

        name = props.get(name_field)
        #code = props.get(code_field)
        short_name = name[:50] if name else "Unnamed"
        
        org_unit = {
            "id": generate_uid(),
            "name": name,
            "shortName": short_name,
            #"code": code,
            "openingDate": str(date.today()), # TODO: not sure if required, or if we can try to read this from the input?
            "level": 2,
            "parent": {
                "id": country_uid
            },
            #"featureType": "MULTI_POLYGON" if geom["type"]=="MultiPolygon" else geom["type"].upper(),
            #"coordinates": geom["coordinates"]
        }
        dhis2_org_units.append(org_unit)

    # Wrap in DHIS2 metadata structure
    dhis2_metadata = {
        "organisationUnits": dhis2_org_units
    }

    # Add the constructed org unit id and metadata attributes to the GeoJSON
    dhis2_geojson = geojson
    org_sub_units = dhis2_org_units[1:] # slightly hacky, skips the country which is added as the first org unit above
    assert len(org_sub_units) == len(geojson['features'])
    for feat,org_unit in zip(geojson['features'], org_sub_units):
        #print(str(feat)[:100], 'vs', str(org_unit)[:100])
        feat['id'] = org_unit['id']
        org_unit.pop('featureType', None)
        org_unit.pop('coordinates', None)
        feat['properties'] = org_unit

    return dhis2_metadata, dhis2_geojson