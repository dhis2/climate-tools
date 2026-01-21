# dhis2eo

[dhis2eo](https://github.com/dhis2/climate-tools) (short for **DHIS2 Earth Observation**) is our utility library for working with earth observation data and data transformation.

For most of the data processing and handling, we currently recommend using the `earthkit` package directly.

This is still a work in progress, and more utilities will be added in the future.

## Using dhis2eo with Python

Note: In its current state, the Python library provides functions to access climate data directly from the source like the Climate Data Store and Climate Hazard Center. It also provides functions to convert earth observation data to a DHIS2 format.

A big part of our focus is also receiving community contributions for generic functions to perform common workflows and climate-operations. See here for [how to contribute to the project](../contribute.md).

More complete API Reference Documentation will be added in the future.

### Examples

See the following examples that use the `dhis2eo` library:

- [Downloading climate data from ERA5-Land](/guides/getting-data/climate-data-store/era5-download)
- [Downloading climate data from CHIRPS](/guides/getting-data/climate-hazards-center/chirps3-download)
- [Downloading population data from WorldPop](/guides/getting-data/worldpop/worldpop-total-download)
- [Importing data values using dhis2-python-client](/guides/import-data/import-data-values)
