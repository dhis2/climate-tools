# xarray

[xarray](https://docs.xarray.dev/) is a widely used open-source Python library for working with labeled, multi-dimensional arrays. It is particularly well suited for climate and environmental data, where variables are often indexed by dimensions such as time, latitude, and longitude.

`xarray` builds on top of NumPy and integrates closely with the scientific Python ecosystem. It provides a high-level interface for reading, manipulating, and analyzing raster and time-series data stored in formats such as NetCDF and GRIB.

In DHIS2 Climate Tools, `xarray` is used as the core data structure for working with gridded climate data after it has been downloaded. Loading climate datasets as `xarray` objects makes it easy to inspect variables, subset data by time or space, and perform aggregation and transformation operations. `xarray` is also supported by the convenient aggregation functions provided by `earthkit`. 

`xarray` also supports working with large datasets through lazy loading and chunked computation, which is important when processing multi-year climate time series.

Key documentation and learning resources:

- [xarray documentation](https://docs.xarray.dev/)
- [xarray User Guide](https://docs.xarray.dev/en/stable/user-guide/index.html)
- [xarray gallery of examples](https://docs.xarray.dev/en/stable/gallery.html)
