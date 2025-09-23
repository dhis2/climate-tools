---
title: Installation
---

The Python library and command-line utilities are distributed under the package name **`dhis2eo`**. 

To install the climate tools Python library, and its associated commandline utilities, you need to install the `dhis2eo` Python package. 

Until we release a stable version, you can install it directly from the latest Github repository:

        $ pip install git+https://github.com/dhis2/climate-tools

The installation includes all necessary dependencies, including relevant components from [earthkit](../tools/earthkit.md) and [dhis2-python-client](../tools/dhis2-python-client.md).

Once installed, you can use both:

- the Python library:

    ```python
    import dhis2eo
    ```

- the CLI tool:

        $ dhis2eo --help

