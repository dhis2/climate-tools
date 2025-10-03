# dhis2eo

[Dhis2eo](https://github.com/dhis2/climate-tools) (short for **DHIS2 Earth Observation**) is our utility library for working with earth observation data and data transformation. 

For most of the data processing and handling, we currently recommend using the `earthkit` package directly. 

This is still a work in progress, and more utilities will be added in the future. 

## Using dhis2eo with Python

Note: In its current state, the Python library is primarily used to get aggregated geospatial data imported into DHIS2. 

A big part of our focus is also receiving community contributions for generic functions to perform common workflows and climate-operations. See here for [how to contribute to the project](../contribute.md). 

More complete API Reference Documentation will be added in the future.

### Examples

See the following examples that use the `dhis2eo` library: 

- [Aggregate Temperature Data](../aggregation/temperature.ipynb)

## Using dhis2eo on the commandline

The Python library also includes a set of commandline (CLI) tools that are made available during install. 
These are typically shorter one-time tasks that aren't necessarily needed in an automated script. 
The available CLI commands are defined inside the `dhis2eo.cli` module. 

### Examples

Coming soon! 
