---
title: Installation
---

The Climate Tools Python library are distributed under the package name **`dhis2eo`**. 

The library has been developed and tested on **Python 3.11**. We recommend using this version for best compatibility, though other versions may also work. 

To install the Climate Tools Python library you need to install the `dhis2eo` Python package. 

Until we release a stable version, you can install it directly from the latest Github repository:

        $ pip install git+https://github.com/dhis2/climate-tools

The installation includes all necessary dependencies, including relevant components from [earthkit](../tools/earthkit.md) and [dhis2-python-client](../tools/dhis2-python-client.md).

Once installed, you can verify that it installed correctly in a Python session:

        >>> import dhis2eo
