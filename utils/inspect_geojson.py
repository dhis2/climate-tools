import os
import sys
import json

def main(geojson_file):
    print(f"File: {os.path.abspath(geojson_file)}")

    # Load your GeoJSON file
    with open(geojson_file, "r") as f:
        geojson = json.load(f)

    # Count number of features
    count = len(geojson['features'])

    # Print file info
    print(f"Feature count: {count}")

    # Print first n rows
    n = 10
    for i,feat in enumerate(geojson['features'][:n]):
        print('-----------')
        print(f'Feature {i+1}:')
        print('Geometry:')
        print(str(feat['geometry'])[:100] + '...')
        print('Properties:')
        print(json.dumps(feat['properties'], indent=2))

if __name__ == '__main__':
    geojson_file = sys.argv[1]
    main(geojson_file)
