---
title: Climate Hazards Center
---

The [Climate Hazards Center (CHC)](https://www.chc.ucsb.edu/), based at the University of California, Santa Barbara, provides open-access climate datasets focused on rainfall monitoring and drought early warning. Their most widely used product is [CHIRPS](https://www.chc.ucsb.edu/data/chirps) (Climate Hazards Group InfraRed Precipitation with Stations), which combines satellite observations with station data to produce high-resolution precipitation estimates over land.

CHC datasets are distributed as publicly accessible files (e.g. GeoTIFF and NetCDF) and do not require authentication or a dedicated API. Data are accessed directly via HTTP and can be streamed for spatial subsets.

The `dhis2eo.data.chc` module contains convenience functions for downloading selected CHC datasets locally. These files can then be opened by `xarray` for downstream analysis. See:

- [How to download CHIRPS v3 climate data](chirps3-download.ipynb)
