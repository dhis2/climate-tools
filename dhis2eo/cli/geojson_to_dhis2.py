import os
import sys
import json
import string
import random
from datetime import date
from pathlib import Path
import geopandas as gpd

from ..integrations.geopandas import geodataframe_to_dhis2_org_units

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
    gdf = gpd.read_file(geojson_file)

    # Convert to dhis2
    dhis2_metadata, dhis2_geojson = geodataframe_to_dhis2_org_units(gdf, country, name_field)

    # Save to JSON
    with open(f"{output_base_path}_dhis2.json", "w") as f:
        json.dump(dhis2_metadata, f, indent=2)

    print(f"DHIS2 metadata saved to '{output_base_path}_dhis2.json'")

    # Save to GeoJSON that can be used for geometry import (subunits only, not country geometry)
    with open(f"{output_base_path}_dhis2.geojson", "w") as f:
        json.dump(dhis2_geojson, f, indent=2)

    print(f"DHIS2 compatible geojson saved to {output_base_path}_dhis2.geojson")

def register_parser(subparsers):
    description = '''Converts a geojson file to a json metadata file and a geometry geojson file
    that can be used to easily setup a new org unit hierarchy using the DHIS2 Import page.'''
    parser = subparsers.add_parser("geojson-to-dhis2", help=description)
    parser.add_argument("geojson_file", help="Path to the GeoJSON File")
    parser.add_argument("country", help="Name to use for the parent org unit, typically a country name")
    parser.add_argument("name_field", help="Field that contains the name of each org unit")
    #parser.set_defaults(func=lambda args: main(args.input, args.output))
