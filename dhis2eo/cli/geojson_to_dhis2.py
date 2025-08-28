import os
import sys
import json
import string
import random
from datetime import date
from pathlib import Path

def main(
    geojson_file, 
    country, 
    name_field
    ):    
    print(f'Converting geojson file {geojson_file} to dhis2 compatible import files')
    org_units = []

    # Output using same base filename relative to current directory
    file_dir,file_name = os.path.split(geojson_file)
    output_base_file = os.path.splitext(file_name)[0] # this is just the file name so relative to current dir
    output_base_path = os.path.abspath(output_base_file)

    # Load your GeoJSON file
    with open(geojson_file, "r") as f:
        geojson = json.load(f)

    # Generate UIDs
    def generate_uid():
        letters = string.ascii_letters  # A-Z, a-z
        chars = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
        return random.choice(letters).upper() + ''.join(random.choices(chars, k=10))

    # Create top-level country org unit
    props = geojson['features'][0]['properties']
    country_uid = generate_uid()
    #country, country_code = props['COUNTRY'], props['GID_0']
    country_org_unit = {
        "id": country_uid,
        "name": country,
        "shortName": country,
        #"code": country_code,
        "openingDate": str(date.today()),
        "level": 1,
        #"featureType": "NONE"
    }
    org_units.append(country_org_unit)

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
            "openingDate": str(date.today()),
            "level": 2,
            "parent": {
                "id": country_uid
            },
            #"featureType": "MULTI_POLYGON" if geom["type"]=="MultiPolygon" else geom["type"].upper(),
            #"coordinates": geom["coordinates"]
        }
        org_units.append(org_unit)

    # Wrap in DHIS2 metadata structure
    dhis2_metadata = {
        "organisationUnits": org_units
    }

    # Save to JSON
    with open(f"{output_base_path}_dhis2.json", "w") as f:
        json.dump(dhis2_metadata, f, indent=2)

    print(f"DHIS2 metadata saved to '{output_base_path}_dhis2.json'")

    # Save to GeoJSON that can be used for geometry import (subunits only)
    geojson_new = geojson
    org_sub_units = org_units[1:] # slightly hacky, skips the country which is added as the first org unit above
    for feat,org_unit in zip(geojson['features'], org_sub_units):
        #print(str(feat)[:100], 'vs', str(org_unit)[:100])
        feat['id'] = org_unit['id']
        org_unit.pop('featureType', None)
        org_unit.pop('coordinates', None)
        feat['properties'] = org_unit

    with open(f"{output_base_path}_dhis2.geojson", "w") as f:
        json.dump(geojson_new, f, indent=2)

    print(f"DHIS2 compatible geojson saved to {output_base_path}_dhis2.geojson")

def register_parser(subparsers):
    description = '''Converts a geojson file to a json metadata file and a geometry geojson file
    that can be used to easily setup a new org unit hierarchy using the DHIS2 Import page.'''
    parser = subparsers.add_parser("geojson-to-dhis2", help=description)
    parser.add_argument("geojson_file", help="Path to the GeoJSON File")
    parser.add_argument("country", help="Name to use for the parent org unit, typically a country name")
    parser.add_argument("name_field", help="Field that contains the name of each org unit")
    #parser.set_defaults(func=lambda args: main(args.input, args.output))
