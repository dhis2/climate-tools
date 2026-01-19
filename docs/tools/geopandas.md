# geopandas

[geopandas](https://geopandas.org/) is commonly used to work with geospatial vector data. It allows you to work with points, lines, and polygons in a tabular format, where each row represents a geographic feature and includes a geometry column. 

`geopandas` is built on top of [pandas](https://pandas.pydata.org/), a foundational Python library for working with tabular data. 

In DHIS2 Climate Tools, `geopandas` is commonly used to load and manipulate administrative boundaries, such as DHIS2 organisation units, while `pandas` is used to handle the tabular outputs produced by climate data aggregation.

Typical use cases include:

- Loading organisation unit geometries from GeoJSON or Shapefile formats
- Joining spatial data with attribute tables
- Converting aggregated climate values into DHIS2-ready tabular structures

Together, `pandas` and `geopandas` form the bridge between geospatial processing and the tabular data formats required for data import into DHIS2.

Key documentation and learning resources:

- [pandas documentation](https://pandas.pydata.org/docs/)
- [geopandas documentation](https://geopandas.org/en/stable/)
- [geopandas introduction](https://geopandas.org/en/stable/docs/user_guide.html)