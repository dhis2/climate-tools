# Climate Tools

**Climate Tools** is the umbrella project for working with DHIS2 and environmental / climate-related data.  
It includes online documentation, guides, tutorials, and the `dhis2eo` Python package and CLI tool.

Documentation site: https://dhis2.github.io/climate-tools

---

## Installation

The Python library and command-line utilities are distributed under the package name **`dhis2eo`**. 

To install the climate tools Python library, and its associated commandline utilities, you need to install the `dhis2eo` Python package. 

You can install it directly from source (development mode):

        $ git clone https://github.com/dhis2/climate-tools.git
        $ cd climate-tools
        $ pip install -e .

Once installed, you can use both:

- the Python library:

    ```python
    import dhis2
    ```

- the CLI tool:

        $ dhis2eo --help

## Documentation

The climate tools documentation also includes a number of guides and examples for common climate operations and workflows, available at https://dhis2.github.io/climate-tools. This online documentation is built using the MyST web publishing ecosystem (https://mystmd.org/guide/quickstart) and Jupyter notebooks (https://next.jupyterbook.org). The site is automatically updated by making changes to the `docs` folder and pushing to the `main` branch. 

To preview the documentation locally you need to have `Node.js` (https://nodejs.org) installed. Additionally you need to install Jupyter v2: 

        $ pip install --pre "jupyter-book==2.\*"

After installing the dependencies you can run the web server locally:

        $ jupyter book start

You can then browse and preview your local changes:

- Visit localhost:3000 in your browser
