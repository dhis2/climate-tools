---
title: Importing organization unit geometries
short_title: Import org unit geometries
---

Sometimes you don't have access to a desired DHIS2 instance or need to explore different definitions of org unit boundaries in DHIS2, e.g. for testing or debugging purposes. 

This tutorial shows you how to create a new organization unit tree in DHIS2 (possibly for multiple country) by using some of the provided commandline utilities. 

## Prerequisites

The following tutorial assumes the `utils` folder is on your system path [TODO: this should be auto added as part of package install].

## Getting your boundary data

First you need a geojson file containing the administrative boundaries for some country. If you don't already have this,
you can easily fetch some from https://www.geoboundaries.org/countryDownloads.html and unzip its contents. The geojson must be for a single adminstrative level, and will all be linked to a single parent country. 

## Converting your boundary data to DHIS2 format

Inspect the contents of your geojson file, which should print some useful info about the geojson contents:

        >>> inspect_geojson "path/to/file.geojson"

Now that you know the structure and fields of your geojson, you can convert the geojson to the files needed
to upload to DHIS2. The parent country name and code are manually provided as part of the command. The org unit codes should be a field containing ideally something like an ISO code, but can also be any uniquely identifying ID. 

        >>> geojson_to_dhis2 "path/to/file.geojson" "<country_name>" "<name_field>"

The output files will be saved to your current working directory as:

- `path/to/file_dhis2.json` # The JSON metadata file to import the orgunit structure
- `path/to/file_dhis2.geojson` # The GeoJSON file to import the geometries

## Importing into DHIS2

Steps to import the orgunit hierarchy:

1. Go to Import/Export app in DHIS2
2. On the "Metadata import" page, upload the generated file named "<your_file_name>_dhis2.json"
3. Click the Start dry run or import buttons

Steps to import the orgunit geometries (these will be matched to the previously uploaded orgunits):

1. Go to Import/Export app in DHIS2
2. On the "Org unit geometry import" page, upload the generated file named "<your_file_name>_dhis2.geojson"
3. Check the option to "Match GeoJSON property to organisation unit scheme", and input "id" as the property name and select "Id" for ID scheme. [TODO: Check, this may or may not be necessary]
4. Click the Start dry run or import buttons

## Final steps

Finally, before you can do anything with the newly created orgunits, you need to:

1. Update analytics tables from the Data Administration app
2. Make sure to go to the Users app and enable so that your user can view the newly imported orgunit hierarchy tree
